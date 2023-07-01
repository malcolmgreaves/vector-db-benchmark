import time
from typing import List, Optional

from qdrant_client import QdrantClient
from qdrant_client.http.models import Batch, CollectionStatus

from engine.base_client.upload import BaseUploader
from engine.clients.qdrant.config import QDRANT_COLLECTION_NAME


class QdrantUploader(BaseUploader):
    client = None
    upload_params = {}

    
    def init_client(cls, host, distance, connection_params, upload_params):
        cls.client = QdrantClient(host=host, prefer_grpc=True, **connection_params)
        cls.upload_params = upload_params

    
    def upload_batch(
        cls, ids: List[int], vectors: List[list], metadata: Optional[List[dict]]
    ):
        # print("\n\n\n\n\nHERE\n\n\n\n\n\n")
        # import ipdb;
        # ipdb.set_trace()

        # print(f"\n\n{cls=}\n\n")

        cls.client.upsert(
            collection_name=QDRANT_COLLECTION_NAME,
            points=Batch.construct(
                ids=ids,
                vectors=vectors,
                payloads=[payload or {} for payload in metadata],
            ),
        )

    
    def post_upload(cls, _distance):
        cls.wait_collection_green()
        return {}

    
    def wait_collection_green(cls):
        wait_time = 5.0
        total = 0
        while True:
            time.sleep(wait_time)
            total += wait_time
            collection_info = cls.client.get_collection(QDRANT_COLLECTION_NAME)
            if collection_info.status != CollectionStatus.GREEN:
                continue
            time.sleep(wait_time)
            collection_info = cls.client.get_collection(QDRANT_COLLECTION_NAME)
            if collection_info.status == CollectionStatus.GREEN:
                break
        return total

    
    def delete_client(cls):
        if cls.client is not None:
            del cls.client
