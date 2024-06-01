# generated by datamodel-codegen:
#   filename:  gcp_datastore_lookup_api.yaml
#   timestamp: 2024-06-01T15:28:55+00:00

from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class DatastoreEntityRequest(BaseModel):
    datastore_namespace: Optional[str] = Field(None, example='customer_store')
    datastore_kind: Optional[str] = Field(None, example='customer_data_latest_apr')
    datastore_query: Optional[str] = Field(
        None, example="{'account_id': 'x', 'postcode': 'AB1 CD2', 'first_name': 'John'}"
    )


class DatastoreEntityMultipleRequest(BaseModel):
    datastore_namespace: Optional[str] = Field(None, example='customer_store')
    datastore_kind: Optional[str] = Field(None, example='customer_data_latest_apr')
    datastore_query: Optional[str] = Field(
        None, example="{'account_id': 'x', 'postcode': 'AB1 CD2', 'first_name': 'John'}"
    )


class DatastoreEntityResponse(BaseModel):
    json_string_response_entity: Optional[str] = Field(
        None,
        example="{'account_id': 'x', 'insertion_timestamp': '2024-04-25T11:11:55Z'}",
    )


class DatastoreEntityMultipleResponse(BaseModel):
    __root__: List[Dict[str, Any]]


class ErrorResponse(BaseModel):
    exception: str = Field(..., description='exception')
    error_class: Optional[str] = Field(None, description='error message')
