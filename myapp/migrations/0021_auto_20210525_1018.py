# Generated by Django 3.2 on 2021-05-25 04:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0020_myappointment_app_applytime'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myappointment',
            name='app_applytime',
        ),
        migrations.AddField(
            model_name='myappointment',
            name='app_applyTime_Date',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 25, 10, 18, 43, 843032)),
            preserve_default=False,
        ),
    ]