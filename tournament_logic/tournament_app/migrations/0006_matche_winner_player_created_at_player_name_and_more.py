# Generated by Django 5.0.6 on 2024-07-09 17:43

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication_app', '0002_rename_user_profile_profile'),
        ('tournament_app', '0005_alter_tournament_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='matche',
            name='winner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='m_win', to='tournament_app.player'),
        ),
        migrations.AddField(
            model_name='player',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='player',
            name='name',
            field=models.CharField(default='player_x', max_length=100),
        ),
        migrations.AlterField(
            model_name='matche',
            name='player1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='matche_p1', to='tournament_app.player'),
        ),
        migrations.AlterField(
            model_name='matche',
            name='player2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='matche_p2', to='tournament_app.player'),
        ),
        migrations.AlterField(
            model_name='matche',
            name='status',
            field=models.CharField(choices=[('UNP', 'unplayed'), ('PLY', 'played')], default='unplayed', max_length=50),
        ),
        migrations.AlterField(
            model_name='player',
            name='profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='players', to='authentication_app.profile'),
        ),
        migrations.AlterField(
            model_name='player',
            name='won',
            field=models.BooleanField(default=True),
        ),
    ]
