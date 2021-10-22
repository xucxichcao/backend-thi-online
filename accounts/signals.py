from django.db.models.signals import post_save, pre_delete
from accounts.models import CustomUser, Truong
from django.dispatch import receiver


@receiver(post_save, sender=CustomUser)
def createSchool(sender, instance, created, **kwargs):
    if created:
        newTruong = Truong(user=instance)
        newTruong.save()
