# Generated by Django 3.2 on 2025-03-14 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_chatmessage'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmessage',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
    ]
