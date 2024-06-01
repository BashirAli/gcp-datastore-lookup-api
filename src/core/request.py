from database import DatastoreClient
from utils.helper import deduplicate_entities

def get_single_ds_entry( datastore_namespace, datastore_kind, request, pydantic_validation_model):
    datastore = DatastoreClient(datastore_namespace, datastore_kind)

    ds_entries = datastore.get_entity_from_datastore(datastore_kind, request)
    if len(ds_entries) < 1:
        raise Exception("results not found")

    results = []
    for entry in ds_entries:
        results.append(pydantic_validation_model(**entry))

    results = deduplicate_entities(results)
    if len(results) > 1:
        raise Exception("something went wrong with deduplication")

    result = results[0]

    return result


def get_multiple_ds_entries(datastore_namespace, datastore_kind, request, pydantic_validation_model):
    datastore = DatastoreClient(datastore_namespace, datastore_kind)

    ds_entries = datastore.get_entity_from_datastore(datastore_kind, request)
    if len(ds_entries) < 1:
        raise Exception("results not found")

    return pydantic_validation_model(__root__=ds_entries)
