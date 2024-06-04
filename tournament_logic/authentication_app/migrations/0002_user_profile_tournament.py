# Generated by Django 5.0.6 on 2024-06-03 10:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication_app', '0001_initial'),
        ('tournament_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_profile',
            name='tournament',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='players', to='tournament_app.tournament'),
        ),
    ]