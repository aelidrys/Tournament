# Generated by Django 5.0.6 on 2024-07-09 11:19

import django.utils.timezone
import tournament_app.enums
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='tournament',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='four players', max_length=50)),
                ('status', models.CharField(choices=[('PENDING', 'pending'), ('CLOSED', 'closed')], default='pending', max_length=50)),
                ('round', models.CharField(choices=tournament_app.enums.Round.choices, default=4, max_length=50)),
                ('create_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
