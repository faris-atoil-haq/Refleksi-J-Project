from django.db.models.signals import pre_delete
from django.dispatch import receiver

from core.models import Module
from utils.s3_spaces import AWS_S3


# Delete image in bucket after deleting product image object
@receiver(pre_delete, sender=Module)
def delete_image(sender, instance, **kwargs):
    if instance.module_file:
        try:
            AWS_S3().delete_object(instance.module_file.file)
        except Exception as e:
            print("Error: ", e)
