# Generated by Django 4.0.2 on 2022-08-05 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metafeatures', '0009_rename_vidio_link_videoreview_id_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitereview',
            name='career_title',
            field=models.CharField(blank=True, max_length=225),
        ),
    ]
