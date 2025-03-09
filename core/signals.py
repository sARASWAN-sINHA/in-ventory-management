from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from .services.users import UserService

@receiver(post_save, sender=get_user_model())
def assign_user_to_normal_group(sender, instance, created, **kwargs):
    if created:
        UserService.add_user_to_group(instance, "Asset User")