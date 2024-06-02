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

def read_validate_inbound_payload(request):
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

def check_single_result_with_hash(results):
    def make_hashable(value):
        if isinstance(value, list):
            return tuple(value)
        return value

    hashed_values = []

    for item in results:
        # Convert item to a dictionary excluding None values and get the values as a list
        values = list(item.dict(exclude_none=True).values())

        # Make values hashable by converting lists to tuples
        hashable_values = [make_hashable(value) for value in values]

        # Compute the hash of the tuple of hashable values
        hashed_values.append(hash(tuple(hashable_values)))

    # Check if all hashes are the same by converting to a set and checking its length
    return len(set(hashed_values)) == 1
