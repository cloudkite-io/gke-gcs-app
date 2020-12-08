import uuid, logging, os, random, string, sys

from google.cloud import storage

class Gcs(object):
    """
    This class handles the logic for reading and writing to a GCS bucket.
    """
    def __init__(self):
        # Set logging
        logging.basicConfig(stream=sys.stdout, level=logging.INFO)
        # Setup GCS configs
        self.storage_client = storage.Client()

    def upload_blob(self, bucket_name, file_name, contents):
        """Uploads a file to the bucket."""

        bucket = self.storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        blob.upload_from_string(contents)
        print(
            "File {} uploaded to bucket {} as file {}.".format(
                file_name, bucket_name, file_name
            )
        )

if __name__ == '__main__':
    gcs = Gcs()
    bucket = os.getenv('BUCKET')

    # Generate a different file name per job run
    file_name = f"{os.getenv('JOB_NAME')}-{str(uuid.uuid4())}"

    # Generate some random data to upload to GCS
    contents = f"random-contents-{str(uuid.uuid4())}"

    gcs.upload_blob(bucket, file_name, contents)
