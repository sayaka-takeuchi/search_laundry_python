import enum
import os

from google.cloud import storage

from config import get_settings

settings = get_settings()


class BucketName(str, enum.Enum):
    laundry_images = "laundry-images"


def upload_blob(storage_object_name: str, source_file_name: str, bucket_name: str):
    """Uploads a file to the bucket."""
    try:
        storage_client = storage.Client.from_service_account_json(
            settings.google_application_credentials)
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(storage_object_name)

        blob.upload_from_filename(source_file_name)

        print(
            f"File {source_file_name} uploaded to {storage_object_name}."
        )
    finally:
        os.remove(source_file_name)
