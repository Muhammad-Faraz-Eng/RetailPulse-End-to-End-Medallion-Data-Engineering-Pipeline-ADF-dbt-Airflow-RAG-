import os
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient

load_dotenv(dotenv_path="docker/.env")


class ADLSClient:
    def __init__(self):
        self.conn_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        self.client = BlobServiceClient.from_connection_string(self.conn_str)

    def get_container_client(self, container_name):
        return self.client.get_container_client(container_name)

    def list_files(self, container, prefix):
        container_client = self.get_container_client(container)
        return [
            blob.name for blob in container_client.list_blobs(name_starts_with=prefix)
        ]

    def download_file(self, container, blob_name):
        container_client = self.get_container_client(container)
        blob_client = container_client.get_blob_client(blob_name)
        return blob_client.download_blob().readall()

    def upload_file(self, container, blob_name, data):
        container_client = self.get_container_client(container)
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.upload_blob(data, overwrite=True)
