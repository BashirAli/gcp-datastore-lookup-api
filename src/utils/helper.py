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


def format_pydantic_validation_error_message(pydantic_exception: Sequence) -> str:
    exceptions_list = []
    for exception in pydantic_exception:
        parameter = exception["loc"][-1]
        message = exception["msg"]
        exceptions_list.append({"parameter": parameter, "reason": message})
    return f"The following request parameters failed validation: {str(exceptions_list)}"

def create_pydantic_validation_error_message(pydantic_exception: str) -> str:
    exceptions_list = []
    pydantic_exception = pydantic_exception.split("\n")
    pydantic_exception.pop(0)
    # exceptions come in pairs, if the length is an odd number then there is unneeded metadata that can be discarded
    if len(pydantic_exception) % 2 != 0:
        pydantic_exception.pop()

    for i in range(0, len(pydantic_exception), 2):
        exceptions_list.append(
            (pydantic_exception[i], pydantic_exception[i + 1].strip())
        )

    return (
        f"The following request parameters failed validation: {exceptions_list}"
    )