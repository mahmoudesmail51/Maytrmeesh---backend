# Generated by Django 3.2.2 on 2021-06-01 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_package'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='is_served',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='package',
            name='is_served',
            field=models.BooleanField(default=False),
        ),
    ]