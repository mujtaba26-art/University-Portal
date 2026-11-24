
# myapp/signals.py
# from django.db.models.signals import post_save
# from django.dispatch import receiver

# @receiver(post_save, sender=User)
# def user_updated_signal(sender, instance, created, **kwargs):
#     if not created:  # This ensures it's an update, not creation
#         print(f"Model {instance} was updated!")

#         # Put your custom update logic here

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


@receiver(pre_save, sender=User)
def send_reset_link_on_email_change(sender, instance, **kwargs):
    print('password reset')
    try:
        old_user = User.objects.get(pk=instance.pk)
        print(old_user)
    except User.DoesNotExist:
        return  # New user being created, not updated

    if old_user.email != instance.email:
        print('ok')
        uidb64 = urlsafe_base64_encode(force_bytes(instance.pk))
        token = default_token_generator.make_token(instance)


        reset_link = f"{settings.SITE_DOMAIN}/reset/{uidb64}/{token}/"

        send_mail(
            subject="Reset your password",
            message=f"Hi {instance.username},\n\nClick the link to reset your password:\n{reset_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.email],
            fail_silently=False,
        )


from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

@receiver(post_save, sender=Notification)
def notify_users(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'notifications',
            {
                'type': 'send_notification',
                'message': instance.message
            }
        )




# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, TeacherProfile

@receiver(post_save, sender=Message)
def update_unread_message_count(sender, instance, created, **kwargs):
    if created:
        try:
            profile = TeacherProfile.objects.get(user=instance.receiver)
            profile.unread_message_count += 1
            profile.save()
        except TeacherProfile.DoesNotExist:
            pass
