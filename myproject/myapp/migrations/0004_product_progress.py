# Generated by Django 3.2 on 2025-03-19 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_chatmessage_is_read'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='progress',
            field=models.IntegerField(default=0),
        ),
    ]
