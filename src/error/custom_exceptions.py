from pydantic_model.api_model import Message

class DatastoreGenericError(Exception):
    """User Defined Exception for Customer Data fetched from Datastore

    Args:
        Exception ([type]): [description]
    """


class DatastoreNotFoundException(Exception):
    """User Defined Exception for Customer Data fetched from Datastore

        Args:
            Exception ([type]): [description]
        """

class ModelValidationError(Exception):
    """User Defined Exception for Customer Data fetched from Datastore

    Args:
        Exception ([type]): [description]
    """



class DatastoreMultiResultException(Exception):
    """User Defined Exception for Customer Data fetched from Datastore

    Args:
        Exception ([type]): [description]
    """


class InternalAPIException(Exception):
    """User Defined Exception for Internal app exceptions

    Args:
        Exception ([type]): [description]
    """