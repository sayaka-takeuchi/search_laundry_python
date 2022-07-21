import enum
import os

from google.cloud import storage

from config import get_settings

settings = get_settings()


class BucketName(str, enum.Enum):
    laundry_images = "laundry-images"


def upload_blob(storage_object_name: str, source_file_name: str, bucket_name: str):
    """
    Uploads a file to the bucket.
    https://cloud.google.com/storage/docs/samples/storage-upload-file?hl=ja
    """
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


def delete_blob(bucket_name, blob_name):
    """
    Deletes a blob from the bucket.
    https://cloud.google.com/storage/docs/deleting-objects?hl=ja
    """
    # bucket_name = "your-bucket-name"
    # blob_name = "your-object-name"

    storage_client = storage.Client.from_service_account_json(
        settings.google_application_credentials)

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.delete()

    print(f"Blob {blob_name} deleted.")
