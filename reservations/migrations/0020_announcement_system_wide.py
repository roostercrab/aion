# Generated by Django 2.1.2 on 2019-02-01 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0019_auto_20190201_1247'),
    ]

    operations = [
        migrations.AddField(
            model_name='announcement',
            name='system_wide',
            field=models.BooleanField(default=False),
        ),
    ]
