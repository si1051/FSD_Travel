# Generated by Django 4.2.7 on 2023-11-20 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('destinations', '0005_alter_destination_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='destination',
            name='rating',
            field=models.IntegerField(default=0),
        ),
    ]
