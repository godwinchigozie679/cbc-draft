# Generated by Django 4.0.2 on 2022-08-09 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_learning', '0012_alter_course_certifications'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='certifications',
            field=models.TextField(max_length=400),
        ),
    ]
