# Generated by Django 3.0.8 on 2020-08-19 14:30

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0011_remove_post_unlikes'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='likers',
            field=models.ManyToManyField(blank=True, related_name='liked_posts', to=settings.AUTH_USER_MODEL),
        ),
    ]
