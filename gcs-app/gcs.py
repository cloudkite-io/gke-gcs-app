import logging, os, random, string, sys

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

    def upload_blob(self, bucket_name, file_name):
        """Uploads a file to the bucket."""

        bucket = self.storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name) # destination filename
        blob.upload_from_string("This is the default message") #
        print(
            "File {} uploaded to {}.".format(
                file_name, file_name
            )
        )

if __name__ == '__main__':
    gcs = Gcs()
    bucket = os.getenv('BUCKET')
    file_name = os.getenv('JOB_NAME')
    gcs.upload_blob(bucket, file_name)
