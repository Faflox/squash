# Generated by Django 5.1 on 2024-08-23 06:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('table', '0007_finalsmatch_set'),
    ]

    operations = [
        migrations.AlterField(
            model_name='set',
            name='match',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='table.finalsmatch'),
        ),
    ]
