# Generated by Django 2.2.9 on 2020-05-06 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('share', '0015_remove_member_profile_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='member_profile',
            name='name',
            field=models.CharField(default='noname', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='member_profile',
            name='title',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
