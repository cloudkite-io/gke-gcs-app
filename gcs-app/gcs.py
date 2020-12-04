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

    def write_to_file(self, file_name, string_length):
        letters = string.ascii_letters
        message_to_file = ''.join(random.choice(letters) for i in range(string_length))
        print("Random string is:", message_to_file)

        text_file = open(file_name, "w")
        n = text_file.write(message_to_file)
        text_file.close()
        return text_file

    def upload_blob(self, bucket_name, file_name, string_length):
        """Uploads a file to the bucket."""
        self.write_to_file(file_name, string_length)

        bucket = self.storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        blob.upload_from_filename(file_name)
        print(
            "File {} uploaded to {}.".format(
                file_name, file_name
            )
        )

if __name__ == '__main__':
    gcs = Gcs()
    bucket = os.getenv('BUCKET')
    file_name = os.getenv('JOB_NAME')
    string_length = 30
    gcs.upload_blob(bucket, file_name, string_length)
