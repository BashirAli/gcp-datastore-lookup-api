import pytest
import os
import json

from fastapi.testclient import TestClient
from google.cloud import datastore

from config.env import settings
from main import api, self_service_endpoints

CURRENT_PATH = os.path.dirname(__file__)

DUMMY_DATASTORE_CUSTOMER = "customer"
DUMMY_DATASTORE_ACCOUNTS = "account"
@pytest.fixture(scope="session")
def dummy_customer_datastore_data():
    with open(os.path.join(f"{CURRENT_PATH}/data/", 'test_customer_data.json')) as fp:
        datastore_data = json.loads(fp.read())

    return datastore_data


@pytest.fixture(scope="session")
def dummy_accounts_datastore_data():
    with open(os.path.join(f"{CURRENT_PATH}/data/", 'test_account_data.json')) as fp:
        datastore_data = json.loads(fp.read())

    return datastore_data



@pytest.fixture(scope="session")
def mock_datastore(dummy_customer_datastore_data, dummy_accounts_datastore_data):
    """Create a Datastore client and load in our dummy data"""
    mock_datastore = datastore.Client(project=settings.gcp_project_id, namespace=settings.namespace)
    # Load dummy data
    for data in dummy_customer_datastore_data:
        entity_key = mock_datastore.key(DUMMY_DATASTORE_CUSTOMER, f"{data['account_uid']}_{data['account_number']}")
        entity = datastore.Entity(key=entity_key)
        entity.update(**data)
        mock_datastore.put(entity=entity)

    for data in dummy_accounts_datastore_data:
        entity_key = mock_datastore.key(DUMMY_DATASTORE_ACCOUNTS, data["account_uid"])
        entity = datastore.Entity(key=entity_key)
        entity.update(**data)
        mock_datastore.put(entity=entity)

    # Off to the tests
    yield mock_datastore

    # Post testing cleanup
    for data in dummy_customer_datastore_data:
        key = mock_datastore.key(DUMMY_DATASTORE_CUSTOMER, f"{data['account_uid']}_{data['account_number']}")
        mock_datastore.delete(key)

    for data in dummy_accounts_datastore_data:
        key = mock_datastore.key(DUMMY_DATASTORE_ACCOUNTS, data["account_uid"])
        mock_datastore.delete(key)

@pytest.fixture(scope="function")
def api_client(mock_datastore, request):
    """Generate an API test client

    Need to parametrize with a ScheduleModeEnum member, eg:
       @pytest.mark.parametrize("api_client", [ScheduleModeEnum.ALWAYS_ON], indirect=True)
    """
    # Override the datastore dependency in the API for these tests
    api.state.datastore = mock_datastore

    yield TestClient(api)
