# Generated by Django 2.2.9 on 2020-05-07 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('share', '0016_auto_20200506_0813'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member_profile',
            name='title',
        ),
        migrations.AddField(
            model_name='member_profile',
            name='is_moderator',
            field=models.BooleanField(default=False, help_text='Moderators can view and edit all Provisions and Needs'),
        ),
    ]
