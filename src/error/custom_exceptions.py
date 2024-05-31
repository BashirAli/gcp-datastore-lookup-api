from pydantic_model.api_model import Message


class DeadLetterQueueError(Exception):
    """User Defined Exception for DLQ

    Args:
        Exception ([type]): [description]
    """

    def __init__(
        self, original_message: Message, error_description: str, error_stage: str
    ):
        self.original_message = original_message
        self.error_description = error_description
        self.error_stage = error_stage


class SendToReprocessError(Exception):
    """User defined exception to reprocess a message

    Args:
        Exception ([type]): [description]
    """

    def __init__(self, original_message, error_description, error_stage):
        self.original_message = original_message
        self.error_description = error_description
        self.error_stage = error_stage


class MessageDecodeError(Exception):
    """User Defined Exception for Data validation

    Args:
        Exception ([type]): [description]
    """
class MessageValidationError(Exception):
    """User Defined Exception for Data validation

    Args:
        Exception ([type]): [description]
    """


class InternalException(Exception):
    """User Defined Exception for Data validation

    Args:
        Exception ([type]): [description]
    """


class PubsubPublishException(Exception):
    """User Defined Exception for PubSub Publish Exceptions

    Args:
        Exception ([type]): [description]
    """

class DatastoreError(Exception):
    """User Defined Exception for Customer Data fetched from Datastore

    Args:
        Exception ([type]): [description]
    """


class NotFoundException(Exception):
    """User Defined Exception for Customer Data fetched from Datastore

        Args:
            Exception ([type]): [description]
        """


class ValidationError(Exception):
    """User Defined Exception for Customer Data fetched from Datastore

    Args:
        Exception ([type]): [description]
    """


class PydanticValidationError(Exception):
    """User Defined Exception for Customer Data fetched from Datastore

    Args:
        Exception ([type]): [description]
    """



class MultiSearchResultsException(Exception):
    """User Defined Exception for Customer Data fetched from Datastore

    Args:
        Exception ([type]): [description]
    """


class InternalException(Exception):
    """User Defined Exception for Internal app exceptions

    Args:
        Exception ([type]): [description]
    """