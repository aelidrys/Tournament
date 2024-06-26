# Generated by Django 5.0.6 on 2024-06-03 14:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication_app', '0002_user_profile_tournament'),
        ('tournament_app', '0006_alter_tournament_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='matche',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round', models.CharField(choices=[('QUATER', 8), ('HALF', 4), ('FAINAL', 2)], default=4, max_length=50)),
                ('status', models.CharField(choices=[('UNPLAYED', 'unplayed'), ('PLAYED', 'played')], default='unplayed', max_length=50)),
                ('player1', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='p1', to='authentication_app.user_profile')),
                ('player2', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='p2', to='authentication_app.user_profile')),
                ('tourn', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournament_app.tournament')),
            ],
        ),
    ]
