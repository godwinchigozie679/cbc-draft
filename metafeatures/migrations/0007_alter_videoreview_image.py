# Generated by Django 4.0.2 on 2022-08-05 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metafeatures', '0006_videoreview_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videoreview',
            name='image',
            field=models.ImageField(upload_to='courses/video_review'),
        ),
    ]
