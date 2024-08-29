import boto3
from django.conf import settings


class AWS_S3:
    def __init__(self):
        session = boto3.session.Session()
        self.client = session.client('s3',
            endpoint_url=settings.AWS_S3_ENDPOINT_URL, # Find your endpoint in the control panel, under Settings. Prepend "https://".
            region_name=settings.AWS_S3_REGION_NAME, # Use the region in your endpoint.
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID, # Access key pair. You can create access key pairs using the control panel or API.
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY # Secret access key defined through an environment variable.
        )
    
    def delete_object(self, url):
        """Delete an object from the bucket using relative URL path."""
        self.client.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME,  Key=f"{settings.AWS_LOCATION}/{url}")