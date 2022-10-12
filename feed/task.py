import string
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

from celery import shared_task

import time

@shared_task
def create_random_user_accounts(total):
    print("Creating a random user")
    # time.sleep(total)
    print("Done")