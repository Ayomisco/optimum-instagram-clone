# Generated by Django 4.0.4 on 2022-07-08 08:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='First Name')),
                ('last_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Last Name')),
                ('location', models.CharField(blank=True, max_length=50, null=True, verbose_name='Location')),
                ('url', models.URLField(blank=True, max_length=80, null=True)),
                ('profile_info', models.TextField(blank=True, max_length=250, null=True, verbose_name='About Me')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('profile_pic', models.ImageField(blank=True, upload_to='profile_pictures', verbose_name='Picture')),
                ('profile_banner', models.ImageField(blank=True, upload_to='profile_pictures', verbose_name='Picture')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Username')),
            ],
            options={
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profiles',
                'ordering': ['-created_at'],
            },
        ),
    ]