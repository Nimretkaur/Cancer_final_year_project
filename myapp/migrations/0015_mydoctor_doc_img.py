# Generated by Django 3.2 on 2021-05-18 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0014_myreview_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='mydoctor',
            name='doc_img',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
