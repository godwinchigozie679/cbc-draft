# Generated by Django 4.0.2 on 2022-08-09 21:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('e_learning', '0017_alter_modulee_course'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modulee',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_modules', to='e_learning.course'),
        ),
    ]
