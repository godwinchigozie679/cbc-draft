# Generated by Django 4.0.2 on 2022-08-28 08:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0005_authorcommision'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='author_percentage_comm',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='payment.authorcommision'),
        ),
    ]
