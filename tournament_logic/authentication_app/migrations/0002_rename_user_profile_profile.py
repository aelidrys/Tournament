# Generated by Django 5.0.6 on 2024-07-09 11:25

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication_app', '0001_initial'),
        ('tournament_app', '0003_player_profile'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='user_profile',
            new_name='profile',
        ),
    ]