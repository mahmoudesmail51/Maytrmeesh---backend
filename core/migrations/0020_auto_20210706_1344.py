# Generated by Django 3.2.2 on 2021-07-06 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_rename_available_items_available_item'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='available_item',
            name='food_venue',
        ),
        migrations.AddField(
            model_name='available_item',
            name='availablity_time',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
