# Generated by Django 3.2.5 on 2021-07-13 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('animals', '0004_remove_category_friendly_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='animal',
            name='animal_id',
            field=models.IntegerField(default=0),
        ),
    ]
