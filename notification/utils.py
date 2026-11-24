# notifications/utils.py
from main.models import Notification

def create_notification(user, message, url=None):
    return Notification.objects.create(
        user=user,
        message=message,
        url=url
    )