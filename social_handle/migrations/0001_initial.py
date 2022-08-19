# Generated by Django 4.0.2 on 2022-07-26 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SocialHandle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('username_url', models.CharField(max_length=400)),
                ('followers_numbers', models.CharField(max_length=100)),
                ('icon', models.CharField(max_length=150)),
                ('image', models.ImageField(blank=True, null=True, upload_to='social_handle/social_medial_images')),
            ],
        ),
    ]
