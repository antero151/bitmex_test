# Generated by Django 3.0.7 on 2020-06-17 15:48

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20200613_2312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='name',
            field=models.UUIDField(blank=True, default=uuid.UUID('038206c9-07ce-4bff-927e-443031509e9e'), unique=True),
        ),
    ]
