# Generated by Django 2.2.9 on 2020-05-02 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('share', '0007_provision'),
    ]

    operations = [
        migrations.AlterField(
            model_name='provision',
            name='expiration_date',
            field=models.DateTimeField(blank=True, help_text='useful for food and deadlines', null=True),
        ),
    ]
