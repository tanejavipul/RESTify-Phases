# Generated by Django 4.0.3 on 2022-03-10 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0003_ownernotification_restaurantupdate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ownernotification',
            name='time',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='restaurantupdate',
            name='time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]