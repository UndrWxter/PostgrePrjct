# Generated by Django 4.2.7 on 2023-12-20 04:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_favorites'),
    ]

    operations = [
        migrations.AddField(
            model_name='realestate',
            name='liked',
            field=models.IntegerField(default=0),
        ),
    ]