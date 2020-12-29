from django.db.models.signals import post_save, pre_save, post_delete
from .models import Classroom, Company
from django.contrib.auth.models import User, Group
from django.dispatch import receiver



@receiver(post_delete, sender=Classroom)
def on_delete(sender, instance, **kwargs):
    group = Group.objects.get(name=instance.classroom_name)
    group.delete()

