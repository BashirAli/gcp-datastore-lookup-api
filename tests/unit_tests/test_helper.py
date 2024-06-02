
from model.api_model import CustomerResponse, NetworkResponseItem

from utils.helper import create_pydantic_validation_error_message, format_pydantic_validation_error_message, deduplicate_entities, check_single_result_with_hash


@patch("utils.helper.decode_pubsub_message_data")
def test_read_validate_inbound_payload(mock_decode):
    # Configure the mock objects
    # example_data = {"bucket": "test_bucket", "name": "table"}
    # mock_decode.return_value = json.dumps(example_data)
    #
    # mock_request = Message(
    #     message=PubSubMessage(
    #         data=json.dumps(example_data).encode("utf-8"),
    #         message_id="123",
    #         publish_time="2023-07-31T15:01:06.058022+01:00",
    #         attributes={},
    #     )
    # )
    #
    # result = read_validate_inbound_payload(mock_request)
    #
    # # Assert
    # mock_decode.assert_called_with(mock_request.message.data)
    # assert result == CloudStorageEvent(**example_data)
    pass

def test_create_pydantic_validation_error_message():
    message = (
        "1 validation error for IngestionData\ntarget_message_uuid\nField required "
        "[type=missing, input_value={'_table_name': 'wf...41.c000.snappy.parquet'}, "
        "input_type=dict]\nFor further information visit https://errors.pydantic.dev/2.3/v/missing"
    )

    result = create_pydantic_validation_error_message(message)

    assert result == (
        "The following request parameters failed validation: [('target_message_uuid', "
        "\"Field required [type=missing, input_value={'_table_name': "
        "'wf...41.c000.snappy.parquet'}, input_type=dict]\")]"
    )


def test_format_pydantic_validation_error_message():
    test_data = [
        {
            "type": "missing",
            "loc": ("body", "message", "publish_time"),
            "msg": "Field required",
            "input": {
                "data": {
                    "_table_name": "wfm_activity",
                },
                "message_id": "test_message_id",
            },
            "url": "https://errors.pydantic.dev/2.3/v/missing",
        }
    ]
    result = format_pydantic_validation_error_message(test_data)
    assert result == (
        "The following request parameters failed validation: "
        "[{'parameter': 'publish_time', 'reason': 'Field required'}]"
    )


def test_check_single_result_with_hash_false():
    # test_data = [
    #     NetworkResponseItem(ip_address='0.0.0.0', mac_address='mac_add1'),
    #     NetworkResponseItem(ip_address='0.0.0.0', mac_address='mac_add2')
    #
    # ]
    # result = validate_single_result(test_data)
    # assert not result
    pass


def test_check_single_result_with_hash():
    # test_data = [
    #     CustomerResponse(salutation='MR', contact_email_address='johnsmith@vm.co.uk', postcode='AB1 1AB',
    #                      contact_phone_number='02012345678', icoms_account_uid=5123456789,
    #                      last_connect_date='2022-10-02',
    #                      first_name='JOHN', last_name='SMITH', mac_address='mac_add1',
    #                      contact_mobile_number='+44712345678',
    #                      middle_name=None, date_of_birth='2000-01-01', icoms_site_id=5, ip_address='0.0.0.0',
    #                      account_status='Active', icoms_account_number=123456789, service_address_id='867654',
    #                      service_address_04='UK', service_address_02='Some Place', service_address_03='Some County',
    #                      account_type='R', service_address_01='10 Some Road', vm_household_id='192837465',
    #                      service_telephone_number=['01234567890']),
    #     CustomerResponse(salutation='MR', contact_email_address='johnsmith@vm.co.uk', postcode='AB1 1AB',
    #                      contact_phone_number='02012345678', icoms_account_uid=5123456789,
    #                      last_connect_date='2022-10-02',
    #                      first_name='JOHN', last_name='SMITH', mac_address='mac_add1',
    #                      contact_mobile_number='+44712345678',
    #                      middle_name=None, date_of_birth='2000-01-01', icoms_site_id=5, ip_address='0.0.0.0',
    #                      account_status='Active', icoms_account_number=123456789, service_address_id='867654',
    #                      service_address_04='UK', service_address_02='Some Place', service_address_03='Some County',
    #                      account_type='R', service_address_01='10 Some Road', vm_household_id='192837465',
    #                      service_telephone_number=['01234567890']),
    #     CustomerResponse(salutation='MR', contact_email_address='johnsmith@vm.co.uk', postcode='AB1 1AB',
    #                      contact_phone_number='02012345678', icoms_account_uid=5123456789,
    #                      last_connect_date='2022-10-02',
    #                      first_name='JOHN', last_name='SMITH', mac_address='mac_add1',
    #                      contact_mobile_number='+44712345678',
    #                      middle_name=None, date_of_birth='2000-01-01', icoms_site_id=5, ip_address='0.0.0.0',
    #                      account_status='Active', icoms_account_number=123456789, service_address_id='867654',
    #                      service_address_04='UK', service_address_02='Some Place', service_address_03='Some County',
    #                      account_type='R', service_address_01='10 Some Road', vm_household_id='192837465',
    #                      service_telephone_number=['01234567890']),
    # ]
    # result = validate_single_result(test_data)
    #
    # assert result
    pass
