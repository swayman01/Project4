# Generated by Django 2.2.9 on 2020-05-19 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('share', '0023_auto_20200518_0711'),
    ]

    operations = [
        migrations.AlterField(
            model_name='provision',
            name='status',
            field=models.CharField(choices=[('Available', 'available'), ('Pending', 'Pending'), ('Provided', 'provided'), ('Expired', 'expired'), ('Retracted', 'retracted')], default='available', max_length=25),
        ),
    ]