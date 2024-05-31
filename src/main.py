import json
from contextlib import asynccontextmanager
from datetime import datetime
from typing import AsyncGenerator
import pendulum

from fastapi import FastAPI, Request, status, Response, Depends
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from configuration.env import settings
from gcp.pubsub import PubSubPublisher
from gcp.secret import SecretManager
from lib.api import build_hello_world
from configuration.logger_config import logger_config
from service.logger import LoggerAdapter, configure_logger
from service import dependencies
from utils.helper import decode_pubsub_message_data, extract_trace_and_request_type, create_validation_error_list_message
from error.custom_exceptions import (
    DeadLetterQueueError,
    InternalException,
    PubsubPublishException,
    SendToReprocessError,
)
from pydantic_model.api_model import (
    Message,
    EncryptorLog,
    ErrMessageResponse,
    LogStatus,
    GCPTemplateResponse,
    GCPTemplateRequest
)

logger = LoggerAdapter(configure_logger(), None)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    if settings.is_test_env:
        keys = ""
    else:
        sm_client = SecretManager()
        keys = sm_client.get_secret(settings.key_secret_id)
    yield


app = FastAPI(title=settings.api_name, lifespan=lifespan)


@app.get("/health")
def health_check():
    return {"Status": "OK"}

### ### ### ### ### ### PubSub Subscriber ### ### ### ### ### ### ### ###
@app.post("/")
def pubsub_subscriber(request: Message, original_request: Request) -> JSONResponse:

    # set request contexts
    ctx_fields = extract_trace_and_request_type(original_request=original_request)
    original_message = request.model_dump()
    original_message["message"]["data"] = json.loads(
        decode_pubsub_message_data(original_message["message"]["data"], strict=False)
    )
    logger_config.set_request_contexts(
        ctx_fields=ctx_fields, original_message=original_message
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status": "Success",
            "pubsub_message_id": request.message.message_id,
            "pubsub_publish_timestamp": request.message.publish_time,
            "acknowledge_timestamp": str(pendulum.now("Europe/London")),
        },
    )

### ### ### ### ### ### Consumer API ### ### ### ### ### ### ### ###
@app.post("/v1/hello_world")
def gcp_template_response(
        request: GCPTemplateRequest,
        headers: dependencies.HeaderParams = Depends(dependencies.HeaderParams)
):

    response = build_hello_world(request.data)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content= {
            "status": "Success",
            "response": response,
        },
    )



@app.exception_handler(RequestValidationError)
async def api_validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    """Function to handle a validation error on an incoming JSON HTTP request body"""
    validation_exception = create_validation_error_list_message(exc.errors())
    http_response_dict = ErrMessageResponse(
        exception="Request Validation Error", detail=validation_exception
    ).model_dump(exclude_none=True)
    logger.info(
        msg="Request Validation Error Occurred", additional_info=http_response_dict
    )
    try:
        # Handling messages that needs to be sent to DLQ manually
        pubsub_publisher = PubSubPublisher(
            project_id=settings.gcp_project_id, topic=settings.dlq_topic
        )
        pubsub_publisher.publish(
            data=json.loads(
                decode_pubsub_message_data(
                    exc.body["message"].get("data"), strict=False
                )
            ),
            source_message_uuid=exc.body["message"].get("message_id"),
            source_publish_time=exc.body["message"].get("publish_time"),
        )
    except PubsubPublishException as pb:
        http_response_dict = ErrMessageResponse(
            exception="Pubsub Publish Error", detail=str(pb)
        ).model_dump(exclude_none=True)
        logger.info(
            msg=f"PubsubPublishException Error Occurred: {str(pb)}",
            additional_info=http_response_dict,
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=http_response_dict,
        )

    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED, content=http_response_dict
    )


@app.exception_handler(DeadLetterQueueError)
async def dead_letter_queue_exception_handler(
    request: Request, exc: DeadLetterQueueError
):
    """Function to handle a dlq error"""
    try:
        pubsub_message = exc.original_message["message"]
        pubsub_publisher = PubSubPublisher(
            project_id=settings.gcp_project_id, topic=settings.dlq_topic
        )
        pubsub_publisher.publish(
            data=json.loads(
                decode_pubsub_message_data(pubsub_message["data"], strict=False)
            ),
            source_message_uuid=pubsub_message["message_id"],
            source_publish_time=pubsub_message["publish_time"],
        )
    except PubsubPublishException as pb:
        http_response_dict = ErrMessageResponse(
            exception="Pubsub Publish Error", detail=str(pb)
        ).model_dump(exclude_none=True)
        logger.info(
            msg=f"PubsubPublishException Error Occurred: {str(pb)}",
            additional_info=http_response_dict,
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=http_response_dict,
        )

    logger.info(
        msg=f"Unable to process the file - File sent to DLQ.",
        extra_fields=EncryptorLog(
            message_id=pubsub_message["message_id"],
            status=LogStatus.FAILURE,
            source_bucket_name=pubsub_message["attributes"].get("bucketId", None),
            destination_bucket_name=None,
            error_stage=exc.error_stage,
            error_description=exc.error_description,
            response_status_code="202",
            log_timestamp=datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        ).model_dump(),
    )
    http_response_dict = ErrMessageResponse(
        exception="DeadLetterQueueError", detail=str(exc.error_description)
    ).model_dump(exclude_none=True)

    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED, content=http_response_dict
    )


@app.exception_handler(SendToReprocessError)
async def reprocess_message_exception_handler(
    request: Request, exc: SendToReprocessError
):
    """Function to handle reprocess error"""
    logger.error(
        msg=f"Unable to process the message due to internal server error - Message "
        f" will be retried"
    )

    logger.info(
        msg=f"Unable to process the message - Message will be retried",
        extra_fields=EncryptorLog(
            message_id=exc.original_message["message"]["message_id"],
            status=LogStatus.RETRY,
            source_bucket_name=exc.original_message["message"]["attributes"].get(
                "bucketId", None
            ),
            destination_bucket_name=None,
            error_stage=exc.error_stage,
            error_description=exc.error_description,
            response_status_code="500",
            log_timestamp=datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        ).model_dump(),
    )

    http_response_dict = ErrMessageResponse(
        exception="SendToReprocessError", detail=str(exc.error_description)
    ).model_dump(exclude_none=True)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=http_response_dict
    )


@app.exception_handler(InternalException)
async def validation_exception_handler(request: Request, exc: InternalException):
    http_response_dict = ErrMessageResponse(
        exception="Internal Error", detail="Internal Error Occurred"
    ).model_dump(exclude_none=True)
    logger.info(
        msg=f"InternalException Error Occurred: {str(exc)}",
        additional_info=http_response_dict,
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=http_response_dict
    )
