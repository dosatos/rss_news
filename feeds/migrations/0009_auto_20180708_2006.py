# Generated by Django 2.0.7 on 2018-07-08 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0008_auto_20180708_1820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='source',
            name='link',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
