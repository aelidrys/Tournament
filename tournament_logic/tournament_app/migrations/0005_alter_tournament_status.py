# Generated by Django 5.0.6 on 2024-07-09 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament_app', '0004_alter_matche_round_alter_tournament_round'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='status',
            field=models.CharField(choices=[('PN', 'pending'), ('ST', 'start'), ('EN', 'end')], default='pending', max_length=50),
        ),
    ]
