# Generated by Django 4.1.7 on 2023-04-11 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ajaxapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ajax_data',
            name='age',
            field=models.IntegerField(),
        ),
    ]
