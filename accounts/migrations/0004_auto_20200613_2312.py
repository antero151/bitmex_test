# Generated by Django 3.0.7 on 2020-06-13 23:12

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20200613_2300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='name',
            field=models.UUIDField(blank=True, default=uuid.UUID('dae4e666-a41d-4d50-86f4-25de501b836f'), unique=True),
        ),
    ]
