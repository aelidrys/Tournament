# Generated by Django 5.0.6 on 2024-06-03 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament_app', '0005_alter_tournament_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='status',
            field=models.CharField(choices=[('PENDING', 'pending'), ('CLOSED', 'closed')], default='pending', max_length=50),
        ),
    ]
