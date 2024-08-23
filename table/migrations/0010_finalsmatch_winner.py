# Generated by Django 5.1 on 2024-08-23 06:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('table', '0009_set_set_num'),
    ]

    operations = [
        migrations.AddField(
            model_name='finalsmatch',
            name='winner',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='finals_match_winner', to='table.player'),
        ),
    ]
