# Generated by Django 5.0.6 on 2024-07-09 11:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('won', models.BooleanField(default=False)),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trn_players', to='tournament_app.tournament')),
            ],
        ),
        migrations.CreateModel(
            name='matche',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round', models.CharField(choices=[('QUATER', 8), ('HALF', 4), ('FAINAL', 2)], default=4, max_length=50)),
                ('status', models.CharField(choices=[('UNPLAYED', 'unplayed'), ('PLAYED', 'played')], default='unplayed', max_length=50)),
                ('tourn', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matches', to='tournament_app.tournament')),
                ('player1', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='p1', to='tournament_app.player')),
                ('player2', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='p2', to='tournament_app.player')),
            ],
        ),
    ]
