# Generated by Django 4.0.4 on 2022-07-30 08:40

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
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.IntegerField(choices=[(0, 'liked your post'), (1, 'commented your post'), (2, 'send you friend request'), (3, 'added a new post'), (4, 'added a new story')])),
                ('create_on', models.DateTimeField(auto_now_add=True)),
                ('update_on', models.DateTimeField(auto_now=True)),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_user', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-create_on'],
            },
        ),
    ]