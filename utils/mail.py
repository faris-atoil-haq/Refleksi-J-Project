import random
import string

from django.conf import settings
from django.core.mail import send_mail


def send_email(title,destination_email,message):
    send_mail(
        title,
        message,
        settings.EMAIL_HOST_USER,
        [destination_email],
        fail_silently=True
    )
    return True

def generate_random_string(length):
    characters = string.ascii_letters + string.digits  # You can customize the set of characters if needed
    return ''.join(random.choice(characters) for _ in range(length))