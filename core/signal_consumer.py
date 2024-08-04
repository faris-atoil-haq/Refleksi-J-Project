from django.conf import settings
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from core.models import *
from utils.s3_spaces import AWS_S3

# Delete image in bucket after deleting product image object
# if settings.STAGING or settings.PROD:
#     @receiver(pre_delete, sender=)
#     def delete_image(sender, instance, **kwargs):
#         AWS_S3().delete_object(instance.file.url)
