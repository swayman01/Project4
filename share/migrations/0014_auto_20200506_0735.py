# Generated by Django 2.2.9 on 2020-05-06 11:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('share', '0013_member_profile_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='member_profile',
            old_name='name',
            new_name='title',
        ),
    ]
