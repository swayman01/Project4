# Generated by Django 2.2.9 on 2020-05-13 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('share', '0020_auto_20200513_0716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='provision',
            name='status',
            field=models.CharField(choices=[('Available', 'available'), ('Pending', 'pending'), ('Provided', 'provided'), ('Expired', 'expired'), ('Retracted', 'retracted')], default='available', help_text='Used for items that repeat (i.e. at service that can be provided     to one person every week', max_length=25),
        ),
    ]
