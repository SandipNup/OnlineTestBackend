# Generated by Django 2.1.5 on 2019-02-24 03:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subject', '0004_auto_20190214_1030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='image',
            field=models.FileField(default='image.jpeg', upload_to='media/'),
        ),
    ]
