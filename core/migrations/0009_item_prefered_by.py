# Generated by Django 3.2.2 on 2021-05-16 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_delete_favortie_items'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='prefered_by',
            field=models.ManyToManyField(to='core.Customer'),
        ),
    ]