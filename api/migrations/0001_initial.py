# Generated by Django 3.2 on 2021-04-12 09:22

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
                ('dob', models.DateField(blank=True, null=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('access_token', models.CharField(blank=True, max_length=100, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UnsplashProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('string_id', models.CharField(max_length=20)),
                ('numeric_id', models.IntegerField()),
                ('username', models.CharField(max_length=50)),
                ('twitter_username', models.CharField(max_length=50)),
                ('portfolio_url', models.CharField(max_length=1000)),
                ('instagram_username', models.CharField(max_length=50)),
                ('total_collections', models.IntegerField()),
                ('total_likes', models.IntegerField()),
                ('total_photos', models.IntegerField()),
                ('followers_count', models.IntegerField()),
                ('following_count', models.IntegerField()),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.profile')),
            ],
        ),
    ]