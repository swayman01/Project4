# Generated by Django 2.2.9 on 2020-05-06 11:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('share', '0014_auto_20200506_0735'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member_profile',
            name='title',
        ),
    ]
