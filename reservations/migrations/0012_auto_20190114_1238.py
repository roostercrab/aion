# Generated by Django 2.1.2 on 2019-01-14 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0011_auto_20190114_1235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='block',
            name='deleted_on',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='block',
            name='description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='resource',
            name='deleted_on',
            field=models.DateField(blank=True, null=True),
        ),
    ]
