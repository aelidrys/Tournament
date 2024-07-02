# Generated by Django 5.0.6 on 2024-07-01 15:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication_app', '0002_user_profile_tournament'),
        ('tournament_app', '0008_alter_matche_tourn'),
    ]

    operations = [
        migrations.CreateModel(
            name='player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('won', models.BooleanField(default=False)),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trn_players', to='tournament_app.tournament')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player', to='authentication_app.user_profile')),
            ],
        ),
    ]