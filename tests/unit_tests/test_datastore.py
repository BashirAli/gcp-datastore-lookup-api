import json
import pytest

from fastapi.encoders import jsonable_encoder
from google.api_core.exceptions import BadRequest, ServiceUnavailable
from unittest.mock import patch, MagicMock

from model.api_model import CustomerRequest, CustomerContractRequest, NetworkRequest, CustomerMetadata, NetworkMetadata, \
    CustomerResponse, NetworkResponse, CustomerContractResponse, CustomerContractMetadata
from domain.request import get_results, get_results_multiple, get_metadata
from error.exceptions import InternalException
from storage.datastore import get_entity, ds_client


@patch("domain.request.get_metadata")
@patch("storage.datastore.get_entity")
def test_get_result_filtering_multiples(mock_get_entity, mock_get_metadata):
    mock_get_entity.return_value = [
        {'salutation': 'MR', 'contact_email_address': 'johnsmith@vm.co.uk', 'postcode': 'AB1 1AB',
         'contact_phone_number': '02012345678', 'icoms_account_uid': 5123456789, 'last_connect_date': '2022-10-02',
         'first_name': 'JOHN', 'last_name': 'SMITH', 'mac_address': 'mac_add1', 'contact_mobile_number': '+44712345678',
         'middle_name': None, 'date_of_birth': '2000-01-01', 'icoms_site_id': 5, 'ip_address': '0.0.0.0',
         'account_status': 'Active', 'icoms_account_number': 123456789, 'service_address_id': '867654',
         'service_address_04': 'UK', 'service_address_02': 'Some Place', 'service_address_03': 'Some County',
         'account_type': 'R', 'service_address_01': '10 Some Road', 'vm_household_id': '192837465',
         'service_telephone_number': ['01234567890']},
        {'salutation': 'MR', 'contact_email_address': 'johnsmith@vm.co.uk', 'postcode': 'AB1 1AB',
         'contact_phone_number': '02012345678', 'icoms_account_uid': 5123456789, 'last_connect_date': '2022-10-02',
         'first_name': 'JOHN', 'last_name': 'SMITH', 'mac_address': 'mac_add2', 'contact_mobile_number': '+44712345678',
         'middle_name': None, 'date_of_birth': '2000-01-01', 'icoms_site_id': 5, 'ip_address': '0.0.0.0',
         'account_status': 'Active', 'icoms_account_number': 123456789, 'service_address_id': '867654',
         'service_address_04': 'UK', 'service_address_02': 'Some Place', 'service_address_03': 'Some County',
         'account_type': 'R', 'service_address_01': '10 Some Road', 'vm_household_id': '192837465',
         'service_telephone_number': ['01234567890']},
        {'salutation': 'MR', 'contact_email_address': 'johnsmith@vm.co.uk', 'postcode': 'AB1 1AB',
         'contact_phone_number': '02012345678', 'icoms_account_uid': 5123456789, 'last_connect_date': '2022-10-02',
         'first_name': 'JOHN', 'last_name': 'SMITH', 'mac_address': 'mac_add3', 'contact_mobile_number': '+44712345678',
         'middle_name': None, 'date_of_birth': '2000-01-01', 'icoms_site_id': 5, 'ip_address': '0.0.0.0',
         'account_status': 'Active', 'icoms_account_number': 123456789, 'service_address_id': '867654',
         'service_address_04': 'UK', 'service_address_02': 'Some Place', 'service_address_03': 'Some County',
         'account_type': 'R', 'service_address_01': '10 Some Road', 'vm_household_id': '192837465',
         'service_telephone_number': ['01234567890']}
    ]

    result = get_results("customer-profile", CustomerRequest(icoms_account_uid=5123456789), CustomerResponse,
                         CustomerMetadata,
                         "fast_access_data_cache")

    expected_result = {
        'salutation': 'MR', 'contact_email_address': 'johnsmith@vm.co.uk', 'postcode': 'AB1 1AB',
        'contact_phone_number': '02012345678', 'icoms_account_uid': 5123456789,
        'last_connect_date': '2022-10-02', 'first_name': 'JOHN', 'last_name': 'SMITH',
        'contact_mobile_number': '+44712345678', 'middle_name': None, 'date_of_birth': '2000-01-01',
        'icoms_site_id': 5, 'account_status': 'Active', 'icoms_account_number': 123456789, 'service_address_id': 867654,
        'service_address_04': 'UK', 'service_address_02': 'Some Place', 'service_address_03': 'Some County',
        'account_type': 'R', 'service_address_01': '10 Some Road', 'vm_household_id': 192837465,
        'service_category_code': None, 'service_telephone_number': ['01234567890'], 'icoms_premises_id': None,
        'is_volt_customer': None, 'accessibility_flag': None,
    }

    assert jsonable_encoder(result) == expected_result


@patch("domain.request.get_metadata")
@patch("storage.datastore.get_entity")
def test_get_multiple_result(mock_get_entity, mock_get_metadata):
    mock_get_entity.return_value = [
        {'salutation': 'MR', 'contact_email_address': 'johnsmith@vm.co.uk', 'postcode': 'AB1 1AB',
         'contact_phone_number': '02012345678', 'icoms_account_uid': 5123456789, 'last_connect_date': '2022-10-02',
         'first_name': 'JOHN', 'last_name': 'SMITH', 'mac_address': 'mac_add1', 'contact_mobile_number': '+44712345678',
         'middle_name': None, 'date_of_birth': '2000-01-01', 'icoms_site_id': 5, 'ip_address': '0.0.0.0',
         'account_status': 'Active', 'icoms_account_number': 123456789, 'service_address_id': '867654',
         'service_address_04': 'UK', 'service_address_02': 'Some Place', 'service_address_03': 'Some County',
         'account_type': 'R', 'service_address_01': '10 Some Road', 'vm_household_id': '192837465'},
        {'salutation': 'MR', 'contact_email_address': 'johnsmith@vm.co.uk', 'postcode': 'AB1 1AB',
         'contact_phone_number': '02012345678', 'icoms_account_uid': 5123456789, 'last_connect_date': '2022-10-02',
         'first_name': 'JOHN', 'last_name': 'SMITH', 'mac_address': 'mac_add2', 'contact_mobile_number': '+44712345678',
         'middle_name': None, 'date_of_birth': '2000-01-01', 'icoms_site_id': 5, 'ip_address': '0.0.0.0',
         'account_status': 'Active', 'icoms_account_number': 123456789, 'service_address_id': '867654',
         'service_address_04': 'UK', 'service_address_02': 'Some Place', 'service_address_03': 'Some County',
         'account_type': 'R', 'service_address_01': '10 Some Road', 'vm_household_id': '192837465'},
        {'salutation': 'MR', 'contact_email_address': 'johnsmith@vm.co.uk', 'postcode': 'AB1 1AB',
         'contact_phone_number': '02012345678', 'icoms_account_uid': 5123456789, 'last_connect_date': '2022-10-02',
         'first_name': 'JOHN', 'last_name': 'SMITH', 'mac_address': 'mac_add3', 'contact_mobile_number': '+44712345678',
         'middle_name': None, 'date_of_birth': '2000-01-01', 'icoms_site_id': 5, 'ip_address': '0.0.0.0',
         'account_status': 'Active', 'icoms_account_number': 123456789, 'service_address_id': '867654',
         'service_address_04': 'UK', 'service_address_02': 'Some Place', 'service_address_03': 'Some County',
         'account_type': 'R', 'service_address_01': '10 Some Road', 'vm_household_id': '192837465'}
    ]

    mock_get_metadata.return_value = {
        'ip_address_latency': '2022-11-16T13:54:21.646000+00:00',
        'ip_address_policy_tags': [{"pii_data_dev": "high"}],
        'mac_address_latency': '2022-11-16T13:54:21.646000+00:00',
        'mac_address_policy_tags': [{"pii_data_dev": "high"}]

    }

    actual_result = get_results_multiple("network", NetworkRequest(icoms_account_uid=5123456789), NetworkResponse,
                                         NetworkMetadata, "fast_access_data_cache")

    expected_result = [
        {
            'ip_address': '0.0.0.0',
            'mac_address': 'mac_add1',
            'metadata': {
                'ip_address_latency': '2022-11-16T13:54:21.646000+00:00',
                'ip_address_policy_tags': [{"pii_data_dev": "high"}],
                'mac_address_latency': '2022-11-16T13:54:21.646000+00:00',
                'mac_address_policy_tags': [{"pii_data_dev": "high"}]
            }
        },
        {
            'ip_address': '0.0.0.0',
            'mac_address': 'mac_add2',
            'metadata': {
                'ip_address_latency': '2022-11-16T13:54:21.646000+00:00',
                'ip_address_policy_tags': [{"pii_data_dev": "high"}],
                'mac_address_latency': '2022-11-16T13:54:21.646000+00:00',
                'mac_address_policy_tags': [{"pii_data_dev": "high"}]
            }
        },
        {
            'ip_address': '0.0.0.0',
            'mac_address': 'mac_add3',
            'metadata': {
                'ip_address_latency': '2022-11-16T13:54:21.646000+00:00',
                'ip_address_policy_tags': [{"pii_data_dev": "high"}],
                'mac_address_latency': '2022-11-16T13:54:21.646000+00:00',
                'mac_address_policy_tags': [{"pii_data_dev": "high"}]
            }
        }
    ]

    assert jsonable_encoder(actual_result) == expected_result


def test_get_mock():
    mock_query = MagicMock()
    mock_query.fetch.side_effect = [ServiceUnavailable('mock error'),
                                    ServiceUnavailable('mock error'),
                                    ServiceUnavailable('mock error'),
                                    ServiceUnavailable('mock error'),
                                    ["Error resolved"]]
    mock_ds_client = MagicMock()
    mock_ds_client.query.return_value = mock_query

    with patch.object(ds_client, 'query', return_value=mock_query):
        results = get_entity("dummy", {"icom_account_uid": "xxx"})
        assert mock_query.fetch.call_count == 5
        assert results == ["Error resolved"]
