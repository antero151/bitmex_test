# Generated by Django 3.0.7 on 2020-06-13 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='side',
            field=models.CharField(choices=[('Buy', 'Buy'), ('Sell', 'Sell')], max_length=5),
        ),
        migrations.AlterField(
            model_name='order',
            name='timestamp',
            field=models.DateTimeField(),
        ),
    ]
