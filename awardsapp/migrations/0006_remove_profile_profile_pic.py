# Generated by Django 3.2.13 on 2022-06-18 18:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('awardsapp', '0005_alter_profile_profile_pic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='profile_pic',
        ),
    ]