from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class PublicMediaStorage(S3Boto3Storage):
    location = 'static'
    default_acl = 'public-read'
    file_overwrite = False
    
    def url(self, name, *args, **kwargs):
        # Call the parent class url method to get the full URL
        full_url = super().url(name, *args, **kwargs)
        
        # Remove query parameters from the URL
        base_url = full_url.split('?')[0]

        return base_url

class PrivateMediaStorage(S3Boto3Storage):
    location = 'static'
    default_acl = 'private'
    file_overwrite = False
    custom_domain = False

    def url(self, name, *args, **kwargs):
        # Call the parent class url method to get the full URL
        full_url = super().url(name, *args, **kwargs)
        
        # Remove query parameters from the URL
        base_url = full_url.split('?')[0]

        return base_url
    