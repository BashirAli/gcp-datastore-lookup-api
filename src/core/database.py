from google.cloud import datastore
from typing import List

from configuration.settings import settings

class DatastoreClient:
    def __init__(self, datastore_namespace, datastore_kind):
        self._client = datastore.Client(project=settings.gcp_project_id, namespace=datastore_namespace)
        self._datastore_kind = datastore_kind

    def get_entity_from_datastore(self, request: dict, fetch_limit=50) -> List[datastore.entity]:
        query = self._client.query(kind=self._datastore_kind)

        for ds_filter in request:
            query.add_filter(ds_filter, "=", request[ds_filter])

        if fetch_limit >= 50:
            fetch_limit = 50

        result = list(query.fetch(limit=fetch_limit))

        return result
