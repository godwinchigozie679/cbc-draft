# Generated by Django 4.0.2 on 2022-08-09 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_learning', '0010_delete_certification'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='certifications',
            field=models.TextField(default=1, max_length=400),
            preserve_default=False,
        ),
    ]
