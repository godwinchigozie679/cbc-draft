# Generated by Django 4.0.2 on 2022-08-04 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metafeatures', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partners',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
