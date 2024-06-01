from pydantic_model.api_model import Message

class DatastoreGenericError(Exception):
    """Custom Exception for generic issues when data fetched from Datastore

    Args:
        Exception ([type]): [description]
    """


class DatastoreNotFoundException(Exception):
    """Custom Exception for data not found when fetched from Datastore

        Args:
            Exception ([type]): [description]
        """

class ModelValidationError(Exception):
    """Custom Exception for Pydantic Model Validation

    Args:
        Exception ([type]): [description]
    """



class DatastoreMultiResultException(Exception):
    """Custom Exception for multiple entities fetched from Datastore

    Args:
        Exception ([type]): [description]
    """


class InternalAPIException(Exception):
    """Custom Exception for Internal api exceptions

    Args:
        Exception ([type]): [description]
    """