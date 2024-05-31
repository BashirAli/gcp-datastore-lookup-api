import base64
import binascii
import datetime
import io
import json
from typing import Sequence

from fastapi import Request
from pydantic_core import ValidationError

from configuration.env import settings
from configuration.logger_config import logger_config
from error.custom_exceptions import DeadLetterQueueError, MessageDecodeError, MessageValidationError

from gcp.gcs import GoogleCloudStorage
from pydantic_model.api_model import CloudStorageEvent, ErrorStage
from service.logger import LoggerAdapter, configure_logger

logger = LoggerAdapter(configure_logger(), None)

def deduplicate_entities(data):

    return []

def read_validate_message_data(request):
    pass




def extract_trace_and_request_type(original_request: Request) -> dict:
    ctx_required_fields = {}
    # X-Cloud-Trace-Context is for GCP tracing to work
    trace_header = original_request.headers.get("X-Cloud-Trace-Context")
    if trace_header and settings.gcp_project_id:
        trace = trace_header.split("/")
        ctx_required_fields[
            "logging.googleapis.com/trace"
        ] = f"projects/{settings.gcp_project_id}/traces/{trace[0]}"

    ctx_required_fields["requestType"] = original_request.scope["path"]
    return ctx_required_fields

def create_validation_error_list_message(pydantic_exception: Sequence) -> str:
    validation_exceptions = []
    for exception in pydantic_exception:
        parameter = exception["loc"][-1]
        message = exception["msg"]
        validation_exceptions.append({"parameter": parameter, "reason": message})
    return f"The following request parameters failed validation: {str(validation_exceptions)}"

def create_validation_error_str_message(pydantic_exception: str) -> str:
    validation_exceptions = []
    pydantic_exception = pydantic_exception.split("\n")
    pydantic_exception.pop(0)
    # exceptions come in pairs, if the length is an odd number then there is unneeded metadata that can be discarded
    if len(pydantic_exception) % 2 != 0:
        pydantic_exception.pop()

    for i in range(0, len(pydantic_exception), 2):
        validation_exceptions.append(
            (pydantic_exception[i], pydantic_exception[i + 1].strip())
        )

    return (
        f"The following request parameters failed validation: {validation_exceptions}"
    )