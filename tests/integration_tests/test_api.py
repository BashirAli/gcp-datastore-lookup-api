import pytest

from unittest.mock import patch
from requests.exceptions import InvalidHeader

from error.exceptions import InternalException

VALID_CUSTOMER_REQUEST_COMBINATIONS = [
    ["vm_household_id"],
    ["icoms_account_uid"],
    ["icoms_account_number", "icoms_site_id"],
    ["contact_email_address"],
    ["contact_email_address", "postcode"],
    ["last_name", "postcode"],
    ["icoms_site_id", "last_name", "postcode", "icoms_premises_id"],
    ["last_name", "postcode", "service_telephone_number"],
    ["icoms_account_number", "icoms_site_id", "last_name", "postcode", "service_telephone_number"],
    ["service_telephone_number"]
]
VALID_NETWORK_REQUEST_COMBINATIONS = [
    ["icoms_account_uid"]
]

VALID_CUSTOMER_CONTRACT_REQUEST_COMBINATIONS = [
    ["icoms_account_uid"]
]

VALID_P2P_REQUEST_COMBINATIONS = [
    ["icoms_account_uid"]
]

headers = {
    "dapi-requestid": "f81d4fae-8jan-22e5-a765-00a0c91e7ee7",
    "dapi-requesttimestamp": "2021-09-17T16:46:47Z",
    "dapi-appid": "MS_PRIME_BUNDLE_BUILDER_STG",
    "dapi-channelid": "WEB",
    "dapi-correlationid": 'e38f8d58-4897-4faa-be63-f8589a635e43'
}

METADATA_DATA_CUSTOMER = {
    'salutation_latency': '2022-11-16T13:54:21.646000+00:00',
    'contact_email_address_latency': '2022-11-16T13:54:21.646000+00:00',
    'postcode_latency': '2022-11-16T13:54:21.646000+00:00',
    'contact_phone_number_latency': '2022-11-16T13:54:21.646000+00:00',
    'icoms_account_uid_latency': '2022-11-16T13:54:21.646000+00:00',
    'last_connect_date_latency': '2022-11-16T13:54:21.646000+00:00',
    'first_name_latency': '2022-11-16T13:54:21.646000+00:00',
    'last_name_latency': '2022-11-16T13:54:21.646000+00:00',
    'contact_mobile_number_latency': '2022-11-16T13:54:21.646000+00:00',
    'middle_name_latency': '2022-11-16T13:54:21.646000+00:00',
    'date_of_birth_latency': '2022-11-16T13:54:21.646000+00:00',
    'icoms_site_id_latency': None,
    'account_status_latency': None,
    'icoms_account_number_latency': None,
    'service_address_id_latency': None,
    'service_address_04_latency': None,
    'service_address_02_latency': None,
    'service_address_03_latency': None,
    'account_type_latency': None,
    'service_address_01_latency': None,
    'vm_household_id_latency': None,
    'service_category_code_latency': None,
    'service_telephone_number_latency': None,
    'accessibility_flag_latency': None,
    'icoms_premises_id_latency': None,
    'is_volt_customer_latency': None,

}

METADATA_DATA_CUSTOMER_POLICY_TAGS = {
    'salutation_policy_tags': [],
    'contact_email_address_policy_tags': [{"pii_data_dev": "high"}],
    'postcode_policy_tags': [{"pii_data_dev": "high"}],
    'contact_phone_number_policy_tags': [{"pii_data_dev": "high"}],
    'icoms_account_uid_policy_tags': [],
    'last_connect_date_policy_tags': [],
    'first_name_policy_tags': [{"pii_data_dev": "high"}],
    'last_name_policy_tags': [{"pii_data_dev": "high"}],
    'contact_mobile_number_policy_tags': [{"pii_data_dev": "high"}],
    'middle_name_policy_tags': [{"pii_data_dev": "high"}],
    'date_of_birth_policy_tags': [{"pii_data_dev": "high"}],
    'icoms_site_id_policy_tags': [],
    'account_status_policy_tags': [],
    'icoms_account_number_policy_tags': [],
    'service_address_id_policy_tags': [],
    'service_address_04_policy_tags': [{"pii_data_dev": "high"}],
    'service_address_02_policy_tags': [{"pii_data_dev": "high"}],
    'service_address_03_policy_tags': [{"pii_data_dev": "high"}],
    'account_type_policy_tags': [],
    'service_address_01_policy_tags': [{"pii_data_dev": "high"}],
    'vm_household_id_policy_tags': [],
    'service_category_code_policy_tags': [],
    'service_telephone_number_policy_tags': [],
    'accessibility_flag_policy_tags': [],
    'icoms_premises_id_policy_tags': [],
    'is_volt_customer_policy_tags': []

}

METADATA_DATA_CUSTOMER_CONTRACTS = {
    'icoms_account_uid_latency': '2022-11-16T13:54:21.646000+00:00',
    'contract_service_category_latency': '2022-11-16T13:54:21.646000+00:00',
    'contract_term_latency': '2022-11-16T13:54:21.646000+00:00',
    'contract_start_date_latency': '2022-11-16T13:54:21.646000+00:00',
    'contract_end_date_latency': '2022-11-16T13:54:21.646000+00:00'
}

METADATA_DATA_CUSTOMER_CONTRACTS_POLICY_TAGS = {
    'icoms_account_uid_policy_tags': [{'taxonomy_name': 'policy_tag_name'}],
    'contract_service_category_policy_tags': [{'taxonomy_name': 'policy_tag_name'}],
    'contract_term_policy_tags': [{'taxonomy_name': 'policy_tag_name'}],
    'contract_start_date_policy_tags': [{'taxonomy_name': 'policy_tag_name'}],
    'contract_end_date_policy_tags': [{'taxonomy_name': 'policy_tag_name'}]
}

METADATA_DATA_NETWORK = {
    'ip_address_latency': '2022-11-16T13:54:21.646000+00:00',
    'mac_address_latency': '2022-11-16T13:54:21.646000+00:00'
}

METADATA_DATA_NETWORK_POLICY_TAGS = {
    'ip_address_policy_tags': [{"pii_data_dev": "high"}],
    'mac_address_policy_tags': [{"pii_data_dev": "high"}]
}

METADATA_P2P_LATENCY = {
    'icoms_account_uid_latency': '2022-11-16T13:54:21.646000+00:00',
    'customer_collection_cnt_latency': '2022-11-16T13:54:21.646000+00:00',
    'invoice_datetime_latency': '2022-11-16T13:54:21.646000+00:00',
    'last_collection_activity_code_latency': '2022-11-16T13:54:21.646000+00:00',
    'last_collection_comment_text_latency': '2022-11-16T13:54:21.646000+00:00',
    'contact_datetime_latency': '2022-11-16T13:54:21.646000+00:00',
    'customer_ptp_cnt_latency': '2022-11-16T13:54:21.646000+00:00',
    'credit_to_date_latency': '2022-11-16T13:54:21.646000+00:00',
    'promise_to_pay_status_latency': '2022-11-16T13:54:21.646000+00:00',
    'promise_pay_by_date_latency': '2022-11-16T13:54:21.646000+00:00',
    'ptp_date_created_latency': '2022-11-16T13:54:21.646000+00:00',
    'promise_amount_latency': '2022-11-16T13:54:21.646000+00:00',
    'a_r_31_60_latency': '2022-11-16T13:54:21.646000+00:00',
    'w_o_type_latency': '2022-11-16T13:54:21.646000+00:00',
    'a_r_balance_latency': '2022-11-16T13:54:21.646000+00:00',
    'w_o_datetime_entered_latency': '2022-11-16T13:54:21.646000+00:00',
    'w_o_scheduled_for_date_latency': '2022-11-16T13:54:21.646000+00:00',
}
MEATDATA_P2P_POLICY_TAGS = {
    'icoms_account_uid_policy_tags': [],
    'customer_collection_cnt_policy_tags': [],
    'invoice_datetime_policy_tags': [],
    'last_collection_activity_code_policy_tags': [],
    'last_collection_comment_text_policy_tags': [],
    'contact_datetime_policy_tags': [],
    'customer_ptp_cnt_policy_tags': [],
    'credit_to_date_policy_tags': [],
    'promise_to_pay_status_policy_tags': [],
    'promise_pay_by_date_policy_tags': [],
    'ptp_date_created_policy_tags': [],
    'promise_amount_policy_tags': [],
    'a_r_31_60_policy_tags': [],
    'a_r_balance_policy_tags': [],
    'w_o_type_policy_tags': [],
    'w_o_datetime_entered_policy_tags': [],
    'w_o_scheduled_for_date_policy_tags': []
}

headers_complete = {
    "dapi-requestid": "f81d4fae-8jan-22e5-a765-00a0c91e7ee7",
    "dapi-requesttimestamp": "2021-09-17T16:46:47Z",
    "dapi-appid": "MS_PRIME_BUNDLE_BUILDER_STG",
    "dapi-channelid": "WEB",
    "dapi-correlationid": 'e38f8d58-4897-4faa-be63-f8589a635e43'
}

headers_not_in_order = {
    "dapi-correlationid": 'e38f8d58-4897-4faa-be63-f8589a635e43',
    "dapi-requestid": "f81d4fae-8jan-22e5-a765-00a0c91e7ee7",
    "dapi-requesttimestamp": "2021-09-17T16:46:47Z",
    "dapi-channelid": "WEB",
    "dapi-appid": "MS_PRIME_BUNDLE_BUILDER_STG"
}

headers_timestamp_wrong_format = {
    "dapi-correlationid": 'e38f8d58-4897-4faa-be63-f8589a635e43',
    "dapi-requestid": "f81d4fae-8jan-22e5-a765-00a0c91e7ee7",
    "dapi-requesttimestamp": "2021-09-17",
    "dapi-channelid": "WEB",
    "dapi-appid": "MS_PRIME_BUNDLE_BUILDER_STG"
}

headers_timestamp_wrong_type = {
    "dapi-correlationid": 'e38f8d58-4897-4faa-be63-f8589a635e43',
    "dapi-requestid": "f81d4fae-8jan-22e5-a765-00a0c91e7ee7",
    "dapi-requesttimestamp": 20210917,
    "dapi-channelid": "WEB",
    "dapi-appid": "MS_PRIME_BUNDLE_BUILDER_STG"
}

headers_correlationid_wrong_type = {
    "dapi-correlationid": 123456789012345678901234567890123456,
    "dapi-requestid": "f81d4fae-8jan-22e5-a765-00a0c91e7ee7",
    "dapi-requesttimestamp": "2021-09-17",
    "dapi-channelid": "WEB",
    "dapi-appid": "MS_PRIME_BUNDLE_BUILDER_STG"
}


def test_get_customer_with_icoms_account_uid(api_client):
    result = api_client.post("/v1/customer-profile", json={"icoms_account_uid": 5123456789}, headers=headers)
    result = result.json()
    assert result == {
        "icoms_account_uid": 5123456789,
        "icoms_account_number": 1123456789,
        "icoms_site_id": 5,
        "account_status": "Active",
        "last_connect_date": "2022-10-02",
        "account_type": "R",
        "vm_household_id": 192837465,
        "salutation": "MR",
        "first_name": "JOHN",
        "middle_name": None,
        "last_name": "SMITH",
        "date_of_birth": "2000-01-01",
        "contact_email_address": "johnsmith@vm.co.uk",
        "contact_phone_number": "02012345678",
        "contact_mobile_number": "+44712345678",
        "service_address_id": 867654,
        "service_address_01": "10 Some Road",
        "service_address_02": "Some Place",
        "service_address_03": "Some County",
        "service_address_04": "UK",
        "postcode": "AB1 1AB",
        "service_category_code": "BB - TV - TELCO",
        "service_telephone_number": ["01012987347"],
        'icoms_premises_id': 5867654,
        'is_volt_customer': 0,
        'accessibility_flag': "ST0000",
        "metadata": {**METADATA_DATA_CUSTOMER, **METADATA_DATA_CUSTOMER_POLICY_TAGS}
    }


def test_get_customer_contracts_with_icoms_account_uid(api_client):
    result = api_client.post("/v1/customer-contracts", json={"icoms_account_uid": 5123456789},
                                                headers=headers)
    result = result.json()
    expected_result = [{
        'icoms_account_uid': 5123456789,
        'contract_service_category': 'BB - TV - TELCO',
        'contract_term': 12345,
        'contract_start_date': '2022-10-02',
        'contract_end_date': '2024-10-02',
        "metadata": {**METADATA_DATA_CUSTOMER_CONTRACTS, **METADATA_DATA_CUSTOMER_CONTRACTS_POLICY_TAGS}
    }]
    assert result == expected_result


def test_get_promise_to_pay_with_icoms_account_uid(api_client):
    result = api_client.post("/v1/promise-to-pay", json={"icoms_account_uid": 5123456789}, headers=headers)
    result = result.json()
    expected_result = [
    {
        "icoms_account_uid": 5123456789,
        "customer_collection_cnt": 2.3,
        "invoice_datetime": "2023-06-23T09:57:29",
        "last_collection_activity_code": "K",
        "last_collection_comment_text": "Purged from Collections Master File",
        "contact_datetime": "2023-06-23T09:57:29",
        "customer_ptp_cnt": 2.0,
        "credit_to_date": 0.5,
        "promise_to_pay_status": "",
        "promise_pay_by_date": None,
        "ptp_date_created": None,
        "promise_amount": 0.0,
        "a_r_31_60": 0.5,
        "a_r_balance": 4.0,
        "w_o_type": "NP",
        "w_o_datetime_entered": "2023-06-23T09:57:29",
        "w_o_scheduled_for_date": "2023-06-23T09:57:29",
        "metadata": {**METADATA_P2P_LATENCY, **MEATDATA_P2P_POLICY_TAGS}
    },
    {
        "icoms_account_uid": 5123456789,
        "customer_collection_cnt": 3.5,
        "invoice_datetime": "2023-06-23T09:57:29",
        "last_collection_activity_code": "K",
        "last_collection_comment_text": "Purged from Collections Master File",
        "contact_datetime": "2023-06-23T09:57:29",
        "customer_ptp_cnt": 0.1,
        "credit_to_date": 0.2,
        "promise_to_pay_status": "",
        "promise_pay_by_date": None,
        "ptp_date_created": None,
        "promise_amount": 0.9,
        "a_r_31_60": 1.0,
        "a_r_balance": 10.7,
        "w_o_type": "NP",
        "w_o_datetime_entered": "2023-06-23T09:57:29",
        "w_o_scheduled_for_date": "2023-06-23T09:57:29",
        "metadata": {**METADATA_P2P_LATENCY, **MEATDATA_P2P_POLICY_TAGS}
    }]
    assert result == expected_result



def test_get_customer_with_icoms_account_number_and_site_id(api_client):
    result = api_client.post(
        "/v1/customer-profile",
        json={"icoms_account_number": "1123456789", "icoms_site_id": 5},
        headers=headers
    )
    result = result.json()
    assert result == {
        "icoms_account_uid": 5123456789,
        "icoms_account_number": 1123456789,
        "icoms_site_id": 5,
        "account_status": "Active",
        "last_connect_date": "2022-10-02",
        "account_type": "R",
        "vm_household_id": 192837465,
        "salutation": "MR",
        "first_name": "JOHN",
        "middle_name": None,
        "last_name": "SMITH",
        "date_of_birth": "2000-01-01",
        "contact_email_address": "johnsmith@vm.co.uk",
        "contact_phone_number": "02012345678",
        "contact_mobile_number": "+44712345678",
        "service_address_id": 867654,
        "service_address_01": "10 Some Road",
        "service_address_02": "Some Place",
        "service_address_03": "Some County",
        "service_address_04": "UK",
        "postcode": "AB1 1AB",
        "service_category_code": "BB - TV - TELCO",
        "service_telephone_number": ["01012987347"],
        'icoms_premises_id': 5867654,
        'is_volt_customer': 0,
        'accessibility_flag': "ST0000",
        "metadata": {**METADATA_DATA_CUSTOMER, **METADATA_DATA_CUSTOMER_POLICY_TAGS}
    }


def test_get_customer_with_only_icoms_account_number(api_client):
    result = api_client.post("/v1/customer-profile", json={"icoms_account_number": "123456789"}, headers=headers)
    result_json = result.json()
    assert result_json == {
        "exception": "Request Body Validation Error Occurred",
        "detail": f"Invalid request parameter combination. Valid combinations: "
                  f"{str(VALID_CUSTOMER_REQUEST_COMBINATIONS)}. Request parameters received: icoms_account_number"
    }
    assert result.status_code == 400


def test_get_customer_contracts_with_icoms_account_number(api_client):
    result = api_client.post("/v1/customer-contracts", json={"icoms_account_number": "123456789"},
                                                headers=headers)
    result_json = result.json()
    assert result_json == {
        "exception": "Request Validation Error Occurred",
        "detail": "The following request parameters failed validation: [('icoms_account_uid', 'field required "
                  "(type=value_error.missing)')]"
    }


def test_get_customer_with_email(api_client):
    result = api_client.post("/v1/customer-profile", json={"contact_email_address": "johnsmith@vm.co.uk"},
                             headers=headers)
    result = result.json()
    assert result == {
        "icoms_account_uid": 5123456789,
        "icoms_account_number": 1123456789,
        "icoms_site_id": 5,
        "account_status": "Active",
        "last_connect_date": "2022-10-02",
        "account_type": "R",
        "vm_household_id": 192837465,
        "salutation": "MR",
        "first_name": "JOHN",
        "middle_name": None,
        "last_name": "SMITH",
        "date_of_birth": "2000-01-01",
        "contact_email_address": "johnsmith@vm.co.uk",
        "contact_phone_number": "02012345678",
        "contact_mobile_number": "+44712345678",
        "service_address_id": 867654,
        "service_address_01": "10 Some Road",
        "service_address_02": "Some Place",
        "service_address_03": "Some County",
        "service_address_04": "UK",
        "postcode": "AB1 1AB",
        "service_category_code": "BB - TV - TELCO",
        "service_telephone_number": ["01012987347"],
        'icoms_premises_id': 5867654,
        'is_volt_customer': 0,
        'accessibility_flag': "ST0000",
        "metadata": {**METADATA_DATA_CUSTOMER, **METADATA_DATA_CUSTOMER_POLICY_TAGS}
    }


def test_get_customer_with_invalid_email(api_client):
    result = api_client.post("/v1/customer-profile", json={"contact_email_address": "johnsmith@vm"}, headers=headers)
    result_json = result.json()
    assert result_json == {
        "exception": "Request Validation Error Occurred",
        "detail": "The following request parameters failed validation: [('contact_email_address', 'value is not a "
                  "valid email address (type=value_error.email)')]"
    }
    assert result.status_code == 400


def test_get_customer_contracts_with_invalid_icoms_account_uuid(api_client):
    result = api_client.post("/v1/customer-contracts", json={"icoms_account_uid": 11111},
                                                headers=headers)
    result_json = result.json()
    assert result_json == {
        "exception": "Request Validation Error Occurred",
        "detail": "The following request parameters failed validation: [('icoms_account_uid', 'ensure this value is "
                  "greater than or equal to 100000000 (type=value_error.number.not_ge; limit_value=100000000)')]"
    }
    assert result.status_code == 400


def test_get_customer_with_email_and_postcode(api_client):
    result = api_client.post(
        "/v1/customer-profile",
        json={"contact_email_address": "tommark@vm.co.uk", "postcode": "WQ1 1QW"},
        headers=headers
    )
    result_json = result.json()
    assert result_json == {
        "icoms_account_uid": 20689841234,
        "icoms_account_number": 5689841234,
        "icoms_site_id": 20,
        "account_status": "Active",
        "last_connect_date": "2022-10-02",
        "account_type": "R",
        "vm_household_id": 6895231234,
        "salutation": "MR",
        "first_name": "TOM",
        "middle_name": None,
        "last_name": "MARK",
        "date_of_birth": "2000-12-12",
        "contact_email_address": "tommark@vm.co.uk",
        "contact_phone_number": "02432145678",
        "contact_mobile_number": "+44712341234",
        "service_address_id": 456987,
        "service_address_01": "10 Some Road",
        "service_address_02": "Some Place",
        "service_address_03": "Some County",
        "service_address_04": "UK",
        "postcode": "WQ1 1QW",
        "service_category_code": "BB - TV - TELCO",
        "service_telephone_number": ["01234567890"],
        'icoms_premises_id': 20456987,
        'is_volt_customer': 0,
        'accessibility_flag': "ST0000",
        "metadata": {**METADATA_DATA_CUSTOMER, **METADATA_DATA_CUSTOMER_POLICY_TAGS}
    }
    assert result.status_code == 200
    assert result.status_code != 400
    assert result_json != {
        "errorCode": "2001",
        "exception": "Multi Search Results Error",
        "detail": "Multiple customer-profile search results found, there should only be one record."
    }


def test_get_customer_postcode(api_client):
    result = api_client.post("/v1/customer-profile", json={"postcode": "WQ2 2QW"}, headers=headers)
    result_json = result.json()
    assert result_json == {
        "exception": "Request Body Validation Error Occurred",
        "detail": f"Invalid request parameter combination. Valid combinations: "
                  f"{str(VALID_CUSTOMER_REQUEST_COMBINATIONS)}. Request parameters received: postcode"
    }
    assert result.status_code == 400


def test_get_customer_last_name(api_client):
    result = api_client.post("/v1/customer-profile", json={"last_name": "SMITH"}, headers=headers)
    result_json = result.json()
    assert result_json == {
        "exception": "Request Body Validation Error Occurred",
        "detail": f"Invalid request parameter combination. Valid combinations: "
                  f"{str(VALID_CUSTOMER_REQUEST_COMBINATIONS)}. Request parameters received: last_name"
    }
    assert result.status_code == 400


def test_get_customer_last_name_and_postcode(api_client):
    result = api_client.post("/v1/customer-profile", json={"postcode": "WQ1 1QW", "last_name": "MARK"}, headers=headers)
    result_json = result.json()
    assert result_json == {
        "icoms_account_uid": 20689841234,
        "icoms_account_number": 5689841234,
        "icoms_site_id": 20,
        "account_status": "Active",
        "last_connect_date": "2022-10-02",
        "account_type": "R",
        "vm_household_id": 6895231234,
        "salutation": "MR",
        "first_name": "TOM",
        "middle_name": None,
        "last_name": "MARK",
        "date_of_birth": "2000-12-12",
        "contact_email_address": "tommark@vm.co.uk",
        "contact_phone_number": "02432145678",
        "contact_mobile_number": "+44712341234",
        "service_address_id": 456987,
        "service_address_01": "10 Some Road",
        "service_address_02": "Some Place",
        "service_address_03": "Some County",
        "service_address_04": "UK",
        "postcode": "WQ1 1QW",
        "service_category_code": "BB - TV - TELCO",
        "service_telephone_number": ["01234567890"],
        'icoms_premises_id': 20456987,
        'is_volt_customer': 0,
        'accessibility_flag': "ST0000",
        "metadata": {**METADATA_DATA_CUSTOMER, **METADATA_DATA_CUSTOMER_POLICY_TAGS}
    }
    assert result.status_code == 200


def test_get_customer_last_name_and_icoms_premises_id_and_icoms_site_id_and_postcode(api_client):
    payload = {
        "postcode": "WQ1 1QW",
        "last_name": "MARK",
        "icoms_premises_id": 20456987,
        "icoms_site_id": 20
    }
    result = api_client.post("/v1/customer-profile", json=payload, headers=headers)
    result_json = result.json()
    assert result_json == {
        "icoms_account_uid": 20689841234,
        "icoms_account_number": 5689841234,
        "icoms_site_id": 20,
        "account_status": "Active",
        "last_connect_date": "2022-10-02",
        "account_type": "R",
        "vm_household_id": 6895231234,
        "salutation": "MR",
        "first_name": "TOM",
        "middle_name": None,
        "last_name": "MARK",
        "date_of_birth": "2000-12-12",
        "contact_email_address": "tommark@vm.co.uk",
        "contact_phone_number": "02432145678",
        "contact_mobile_number": "+44712341234",
        "service_address_id": 456987,
        "service_address_01": "10 Some Road",
        "service_address_02": "Some Place",
        "service_address_03": "Some County",
        "service_address_04": "UK",
        "postcode": "WQ1 1QW",
        "service_category_code": "BB - TV - TELCO",
        "service_telephone_number": ["01234567890"],
        'icoms_premises_id': 20456987,
        'is_volt_customer': 0,
        'accessibility_flag': "ST0000",
        "metadata": {**METADATA_DATA_CUSTOMER, **METADATA_DATA_CUSTOMER_POLICY_TAGS}
    }
    assert result.status_code == 200


def test_get_customer_last_name_and_service_telephone_number_and_postcode(api_client):
    payload = {
        "postcode": "WQ1 1QW",
        "last_name": "MARK",
        "service_telephone_number": "01234567890"
    }
    result = api_client.post("/v1/customer-profile", json=payload, headers=headers)
    result_json = result.json()
    assert result_json == {
        "icoms_account_uid": 20689841234,
        "icoms_account_number": 5689841234,
        "icoms_site_id": 20,
        "account_status": "Active",
        "last_connect_date": "2022-10-02",
        "account_type": "R",
        "vm_household_id": 6895231234,
        "salutation": "MR",
        "first_name": "TOM",
        "middle_name": None,
        "last_name": "MARK",
        "date_of_birth": "2000-12-12",
        "contact_email_address": "tommark@vm.co.uk",
        "contact_phone_number": "02432145678",
        "contact_mobile_number": "+44712341234",
        "service_address_id": 456987,
        "service_address_01": "10 Some Road",
        "service_address_02": "Some Place",
        "service_address_03": "Some County",
        "service_address_04": "UK",
        "postcode": "WQ1 1QW",
        "service_category_code": "BB - TV - TELCO",
        "service_telephone_number": ["01234567890"],
        'icoms_premises_id': 20456987,
        'is_volt_customer': 0,
        'accessibility_flag': "ST0000",
        "metadata": {**METADATA_DATA_CUSTOMER, **METADATA_DATA_CUSTOMER_POLICY_TAGS}
    }
    assert result.status_code == 200


def test_get_customer_icoms_account_number_and_icoms_site_id_and_last_name_and_service_telephone_number_and_postcode(api_client):
    payload = {
        "postcode": "WQ1 1QW",
        "last_name": "MARK",
        "service_telephone_number": "01234567890",
        "icoms_account_number": 5689841234,
        "icoms_site_id": 20
    }
    result = api_client.post("/v1/customer-profile", json=payload, headers=headers)
    result_json = result.json()
    assert result_json == {
        "icoms_account_uid": 20689841234,
        "icoms_account_number": 5689841234,
        "icoms_site_id": 20,
        "account_status": "Active",
        "last_connect_date": "2022-10-02",
        "account_type": "R",
        "vm_household_id": 6895231234,
        "salutation": "MR",
        "first_name": "TOM",
        "middle_name": None,
        "last_name": "MARK",
        "date_of_birth": "2000-12-12",
        "contact_email_address": "tommark@vm.co.uk",
        "contact_phone_number": "02432145678",
        "contact_mobile_number": "+44712341234",
        "service_address_id": 456987,
        "service_address_01": "10 Some Road",
        "service_address_02": "Some Place",
        "service_address_03": "Some County",
        "service_address_04": "UK",
        "postcode": "WQ1 1QW",
        "service_category_code": "BB - TV - TELCO",
        "service_telephone_number": ["01234567890"],
        'icoms_premises_id': 20456987,
        'is_volt_customer': 0,
        'accessibility_flag': "ST0000",
        "metadata": {**METADATA_DATA_CUSTOMER, **METADATA_DATA_CUSTOMER_POLICY_TAGS}
    }
    assert result.status_code == 200


def test_get_customer_service_telephone_number(api_client):
    payload = {
        "service_telephone_number": "01234567890"
    }
    result = api_client.post("/v1/customer-profile", json=payload, headers=headers)
    result_json = result.json()
    assert result_json == {
        "icoms_account_uid": 20689841234,
        "icoms_account_number": 5689841234,
        "icoms_site_id": 20,
        "account_status": "Active",
        "last_connect_date": "2022-10-02",
        "account_type": "R",
        "vm_household_id": 6895231234,
        "salutation": "MR",
        "first_name": "TOM",
        "middle_name": None,
        "last_name": "MARK",
        "date_of_birth": "2000-12-12",
        "contact_email_address": "tommark@vm.co.uk",
        "contact_phone_number": "02432145678",
        "contact_mobile_number": "+44712341234",
        "service_address_id": 456987,
        "service_address_01": "10 Some Road",
        "service_address_02": "Some Place",
        "service_address_03": "Some County",
        "service_address_04": "UK",
        "postcode": "WQ1 1QW",
        "service_category_code": "BB - TV - TELCO",
        "service_telephone_number": ["01234567890"],
        'icoms_premises_id': 20456987,
        'is_volt_customer': 0,
        'accessibility_flag': "ST0000",
        "metadata": {**METADATA_DATA_CUSTOMER, **METADATA_DATA_CUSTOMER_POLICY_TAGS}
    }
    assert result.status_code == 200


def test_get_customer_no_results(api_client):
    result = api_client.post(
        "/v1/customer-profile",
        json={"icoms_account_number": "111111111", "icoms_site_id": 5},
        headers=headers
    )
    result_json = result.json()
    assert result.status_code == 404
    assert result_json == {
        "errorCode": "1001",
        "exception": "NotFound Error",
        "detail": "customer-profile not found using icoms_account_number and icoms_site_id"
    }


def test_get_customer_contracts_no_results(api_client):
    result = api_client.post(
        "/v1/customer-contracts",
        json={"icoms_account_uid": "111111111"},
        headers=headers
    )
    result_json = result.json()
    assert result.status_code == 404
    assert result_json == {
        "errorCode": "1001",
        "exception": "NotFound Error",
        "detail": "customer-contracts not found using icoms_account_uid"
    }


def test_get_customer_no_headers(api_client):
    result = api_client.post("/v1/customer-profile", json={"icoms_account_number": "111111111", "icoms_site_id": 5})
    result_json = result.json()
    print(result_json)
    assert result.status_code == 400
    assert result_json == {
        "exception": "Request Validation Error Occurred",
        'detail': "The following request parameters failed validation: [{'parameter': "
                  "'dapi-requestid', 'reason': 'field required'}, {'parameter': "
                  "'dapi-requesttimestamp', 'reason': 'field required'}, "
                  "{'parameter': 'dapi-channelid', 'reason': 'field required'}, "
                  "{'parameter': 'dapi-correlationid', 'reason': 'field required'}]"
    }


def test_get_customer_no_body(api_client):
    result = api_client.post("/v1/customer-profile", headers=headers)
    result_json = result.json()
    assert result.status_code == 400
    assert result_json == {
        "exception": "Request Body Validation Error Occurred",
        "detail": "Request has no body. It must have a body containing any one of these combinations.: [["
                  "'vm_household_id'], ['icoms_account_uid'], ['icoms_account_number', 'icoms_site_id'], "
                  "['contact_email_address'], ['contact_email_address', 'postcode'], ['last_name', "
                  "'postcode'], ['icoms_site_id', 'last_name', 'postcode', 'icoms_premises_id'], "
                  "['last_name', 'postcode', 'service_telephone_number'], "
                  "['icoms_account_number', 'icoms_site_id', 'last_name', 'postcode', 'service_telephone_number'], "
                  "['service_telephone_number']]"
    }


def test_get_customer_multiple_search_results(api_client):
    result = api_client.post("/v1/customer-profile", json={"contact_email_address": "tommark@vm.co.uk"},
                             headers=headers)
    result_json = result.json()
    assert result_json == {"errorCode": "2001", "exception": "Multi Search Results Error",
                           "detail": "Multiple customer-profile search results found, there should only be one record."}

def test_get_network_with_icoms_account_uid(api_client):
    result = api_client.post("/v1/network", json={"icoms_account_uid": "5123456789"}, headers=headers)
    result = result.json()
    assert result == [
        {
            "ip_address": "0.0.0.0",
            "mac_address": "mac_add1",
            "metadata": {**METADATA_DATA_NETWORK, **METADATA_DATA_NETWORK_POLICY_TAGS}
        }
    ]



def test_get_network_with_only_icoms_account_number(api_client):
    result = api_client.post("/v1/network", json={"icoms_account_number": "123456789"}, headers=headers)
    result_json = result.json()
    assert result_json == {
        "exception": "Request Validation Error Occurred",
        "detail": f"The following request parameters failed validation: [('icoms_account_uid', 'field required (type=value_error.missing)')]"}
    assert result.status_code == 400


def test_get_network_multiple_results(api_client):
    result = api_client.post("/v1/network", json={"icoms_account_uid": "20689849032"}, headers=headers)
    result = result.json()
    assert result == [
        {
            "ip_address": "8.8.8.8",
            "mac_address": "mac_add2",
            "metadata": {**METADATA_DATA_NETWORK, **METADATA_DATA_NETWORK_POLICY_TAGS}
        },
        {
            "ip_address": "8.8.4.4",
            "mac_address": "mac_add3",
            "metadata": {**METADATA_DATA_NETWORK, **METADATA_DATA_NETWORK_POLICY_TAGS}
        }
    ]


def test_get_network_no_results(api_client):
    result = api_client.post("/v1/network", json={"icoms_account_uid": "111111111"}, headers=headers)
    result_json = result.json()
    assert result.status_code == 404
    assert result_json == {
        "errorCode": "1001",
        "exception": "NotFound Error",
        "detail": "network not found using icoms_account_uid"
    }


def test_get_network_no_headers(api_client):
    result = api_client.post("/v1/network", json={"icoms_account_uid": "20689849032"})
    result_json = result.json()
    assert result.status_code == 400

    assert result_json == {
        "exception": "Request Validation Error Occurred",
        'detail': "The following request parameters failed validation: [{'parameter': "
                  "'dapi-requestid', 'reason': 'field required'}, {'parameter': "
                  "'dapi-requesttimestamp', 'reason': 'field required'}, "
                  "{'parameter': 'dapi-channelid', 'reason': 'field required'}, "
                  "{'parameter': 'dapi-correlationid', 'reason': 'field required'}]"
    }


def test_get_network_no_body(api_client):
    result = api_client.post("/v1/network", headers=headers)
    result_json = result.json()
    assert result.status_code == 400
    assert result_json == {
        "exception": "Request Body Validation Error Occurred",
        "detail": "Request has no body. It must have a body containing any one of these combinations.: [["
                  "'icoms_account_uid']]"
    }


@patch("storage.datastore.get_entity")
def test_internal_exception_handler(mock_get_entity, api_client):
    mock_get_entity.side_effect = InternalException
    result = api_client.post("/v1/network", json={"icoms_account_uid": "20689849032"}, headers=headers)
    result_json = result.json()
    assert result.status_code == 500

    assert result_json == {
        "exception": "Internal Error Occurred",
        'detail': "Internal Error Occurred"
    }


@patch('domain.request.get_results')
def test_customer_timestamp_wrong_format(mock_get_customer_result, api_client):
    response = api_client.post(
        "/v1/customer-profile",
        json={"contact_email_address": "johnsmith@vm.co.uk"},
        headers=headers_timestamp_wrong_format
    )

    assert response.status_code == 400
    assert response.json() == {
        'detail': "The following request parameters failed validation: [{'parameter': 'dapi-requesttimestamp', 'reason': 'invalid datetime format'}]",
        'exception': 'Request Validation Error Occurred'}


@patch('domain.request.get_results')
def test_customer_timestamp_wrong_type_no_validation_exception_handler(mock_get_customer_result, api_client):
    with pytest.raises(InvalidHeader) as e:
        api_client.post(
            "/v1/customer-profile",
            json={"contact_email_address": "johnsmith@vm.co.uk"},
            headers=headers_timestamp_wrong_type
        )

    assert e, "Should fail with wrong timestamp type - int"
    assert "must be of type str or bytes" in str(e.value)


@patch('domain.request.get_results_multiple')
def test_network_timestamp_wrong_format(mock_get_network_result, api_client):
    response = api_client.post(
        "/v1/network",
        json={"icoms_account_number": "123456789", "icoms_site_id": 5},
        headers=headers_timestamp_wrong_format
    )

    assert response.status_code == 400
    assert response.json() == {
        'detail': "The following request parameters failed validation: [{'parameter': "
                  "'dapi-requesttimestamp', 'reason': 'invalid datetime format'}]",
        'exception': 'Request Validation Error Occurred'
    }


@patch('domain.request.get_results_multiple')
def test_network_timestamp_wrong_type_no_validation_exception_handler(mock_get_network_result, api_client):
    with pytest.raises(InvalidHeader) as e:
        api_client.post(
            "/v1/network",
            json={"icoms_account_number": "123456789", "icoms_site_id": 5},
            headers=headers_timestamp_wrong_type
        )

    assert e, "Should fail with wrong timestamp type - int"
    assert "must be of type str or bytes" in str(e.value)


def test_get_customer_contracts_truncated_icoms_uid(api_client):
    result = api_client.post("/v1/customer-contracts", json={"icoms_account_uid": 51234567},
                             headers=headers)
    result_json = result.json()
    assert result_json == {
        "exception": "Request Validation Error Occurred",
        "detail": "The following request parameters failed validation: [('icoms_account_uid', 'ensure this value is "
                  "greater than or equal to 100000000 (type=value_error.number.not_ge; limit_value=100000000)')]"
    }

def test_get_customer_profile_truncated_icoms_uid(api_client):
    result = api_client.post("/v1/customer-profile", json={"icoms_account_uid": 51234567},
                             headers=headers)
    result_json = result.json()
    assert result_json == {
        "exception": "Request Validation Error Occurred",
        "detail": "The following request parameters failed validation: [('icoms_account_uid', 'ensure this value is "
                  "greater than or equal to 100000000 (type=value_error.number.not_ge; limit_value=100000000)')]"
    }

def test_get_network_truncated_icoms_uid(api_client):
    result = api_client.post("/v1/network", json={"icoms_account_uid": 51234567},
                             headers=headers)
    result_json = result.json()
    assert result_json == {
        "exception": "Request Validation Error Occurred",
        "detail": "The following request parameters failed validation: [('icoms_account_uid', 'ensure this value is "
                  "greater than or equal to 100000000 (type=value_error.number.not_ge; limit_value=100000000)')]"
    }

def test_get_promise_to_pay_truncated_icoms_uid(api_client):
    result = api_client.post("/v1/promise-to-pay", json={"icoms_account_uid": 51234567},
                             headers=headers)
    result_json = result.json()
    assert result_json == {
        "exception": "Request Validation Error Occurred",
        "detail": "The following request parameters failed validation: [('icoms_account_uid', 'ensure this value is "
                  "greater than or equal to 100000000 (type=value_error.number.not_ge; limit_value=100000000)')]"
    }