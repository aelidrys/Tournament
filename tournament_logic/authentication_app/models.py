import os
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import User
from tournament_app.models import tournament
from tournament_app.enums import U_status


# Create your models here.

default_image_path = '/user/app/media/UserPhotos/default.jpg'


class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='UserPhotos/default.jpg',
        upload_to='UserPhotos')
    access_token = models.CharField(max_length=200, null=True, blank=True)
    remote_user = models.BooleanField(default=False)
    status = models.CharField(max_length=50, choices=U_status.choices(),
        default=U_status.ON.value)
    tournament = models.ForeignKey(tournament, related_name="players",
        on_delete=models.SET_NULL, default=None, null=True, blank=True)

    def __str__(self):
        return self.user.username+"_prf"


# delete image when profile deleted
@receiver(models.signals.post_delete, sender=profile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.image and not instance.image.path == default_image_path:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

# delete old image when a new image is selected
@receiver(models.signals.pre_save, sender=profile)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = sender.objects.get(pk=instance.pk).image
    except sender.DoesNotExist:
        return False

    new_file = instance.image
    if not old_file == new_file and old_file.path != default_image_path:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
