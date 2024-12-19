# Generated by Django 3.2.16 on 2024-12-19 01:52

import community.bases.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('comments', '0005_comment_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0006_auto_20241219_1052'),
        ('profiles', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostEmoji',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_active', models.BooleanField(blank=True, default=True, null=True, verbose_name='Is Active')),
                ('is_deleted', models.BooleanField(blank=True, default=False, null=True, verbose_name='Is Deleted')),
                ('deleted', models.DateTimeField(blank=True, null=True, verbose_name='Deleted')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('emoji_code', models.CharField(max_length=255, verbose_name='Emoji Code')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_emojis', to='posts.post', verbose_name='Post')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_emojis', to='profiles.profile', verbose_name='Profile')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_emojis', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Post Emoji',
                'verbose_name_plural': 'Post Emoji',
                'ordering': ['-created'],
            },
            bases=(community.bases.models.UpdateMixin, models.Model),
        ),
        migrations.CreateModel(
            name='CommentEmoji',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_active', models.BooleanField(blank=True, default=True, null=True, verbose_name='Is Active')),
                ('is_deleted', models.BooleanField(blank=True, default=False, null=True, verbose_name='Is Deleted')),
                ('deleted', models.DateTimeField(blank=True, null=True, verbose_name='Deleted')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('emoji_code', models.CharField(max_length=255, verbose_name='Emoji Code')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_emojis', to='comments.comment', verbose_name='Comment')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_emojis', to='profiles.profile', verbose_name='Profile')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_emojis', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Comment Emoji',
                'verbose_name_plural': 'Comment Emoji',
                'ordering': ['-created'],
            },
            bases=(community.bases.models.UpdateMixin, models.Model),
        ),
    ]
