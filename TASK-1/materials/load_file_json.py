from google.cloud import storage
import os


def write_to_gcs(bucket_name, blob_name, data):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    with open(data, 'rb') as file:
        blob.upload_from_file(file)

bucket_name = os.getenv('BUCKET_NAME')
blob_name = 'rifa-task-1.json'
write_to_gcs(bucket_name, blob_name, 'potter.json')

