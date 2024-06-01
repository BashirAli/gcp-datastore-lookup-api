import logging.config
import time
import json
import os

from pydantic_models.models import DatastoreEntityRequest
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from core.request import get_single_ds_entry, get_multiple_ds_entries
from configuration.env import settings
from error.custom_exceptions import (
    InternalAPIException,
    DatastoreGenericError,
    DatastoreNotFoundException,
    ModelValidationError,
    DatastoreMultiResultException,
    InternalAPIException )

app = FastAPI(
    title=settings.api_name,
)
@app.get("/health")
def health_check():
    return {"Status": "OK"}


@app.post("/v1/get_entity")
async def get_entity(request: DatastoreEntityRequest):
    try:
        request_body = await request.json()
        logging.info("connected to single")
    except json.JSONDecodeError:
        raise RequestValidationError('Request has no body. It must have a body')

    #TODO VALIDATE JSON


    entity_response = get_single_ds_entry(request_body["datastore_namespace"], request_body["datastore_kind"], request_body["datastore_query"])

    return entity_response



@app.post("/v1/get_entities")
async def get_entities(request: DatastoreEntityRequest):
    try:
        request_body = await request.json()
        logging.info("connected to multiple")
    except json.JSONDecodeError:
        raise RequestValidationError('Request has no body. It must have a body')

    #TODO VALIDATE JSON

    entity_response = get_multiple_ds_entries(request_body["datastore_namespace"], request_body["datastore_kind"], json.loads(request_body["datastore_query"]))
    # turn list of entities in to list of string dict


    return entity_response



@api.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(msg="RequestValidation Error Occurred")
    validation_exception = create_header_validation_error_message(exc.errors())
    http_response = ErrorResponse(exception="Request Validation Error Occurred", detail=validation_exception)
    http_response_dict = http_response.model_dump(exclude_none=True)
    logger.info(msg=http_response_dict)
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=http_response_dict
    )


@api.exception_handler(ModelValidationError)
async def validation_exception_handler(request: Request, exc: ModelValidationError):
    logger.error(msg="ModelValidation Error Occurred")
    validation_exception = create_validation_error_message(str(exc))
    http_response = ErrorResponse(exception="Request Validation Error Occurred", detail=validation_exception)
    http_response_dict = http_response.model_dump(exclude_none=True)
    logger.info(msg=http_response_dict)
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=http_response_dict
    )


@api.exception_handler(DatastoreGenericError)
async def validation_exception_handler(request: Request, exc: DatastoreGenericError):
    logger.error(msg="DatastoreGeneric Error Occurred")
    http_response = ErrorResponse(exception="Datastore Error", detail=str(exc))
    http_response_dict = http_response.model_dump(exclude_none=True)
    logger.info(msg=http_response_dict)
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=http_response_dict
    )


@api.exception_handler(DatastoreNotFoundException)
async def validation_exception_handler(request: Request, exc: DatastoreNotFoundException):
    logger.error(msg="DatastoreNotFound Error Occurred")
    http_response = ErrorResponse(errorCode="1001", exception="NotFound Error", detail=str(exc))
    http_response_dict = http_response.model_dump(exclude_none=True)
    logger.info(msg=http_response_dict)
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=http_response_dict
    )


@api.exception_handler(DatastoreMultiResultException)
async def validation_exception_handler(request: Request, exc: DatastoreMultiResultException):
    logger.error(msg="DatastoreMultiResult Exception Occurred")
    http_response = ErrorResponse(errorCode="2001", exception="Multi Search Results Error", detail=str(exc))
    http_response_dict = http_response.model_dump(exclude_none=True)
    logger.info(msg=http_response_dict)
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=http_response_dict
    )


@api.exception_handler(InternalAPIException)
async def validation_exception_handler(request: Request, exc: InternalAPIException):
    # Log the actual error but return a generic response to the consumer
    logger.error(msg=f"InternalAPI Exception Occurred: {str(exc)}")
    http_response = ErrorResponse(exception="Internal Error Occurred", detail="Internal Error Occurred")
    http_response_dict = http_response.model_dump(exclude_none=True)
    logger.info(msg=http_response_dict)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=http_response_dict
    )