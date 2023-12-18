# Generated by Django 3.2.16 on 2023-12-18 10:42

import community.apps.community_medias.models.index
import community.bases.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('communities', '0006_alter_community_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommunityMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_active', models.BooleanField(blank=True, default=True, null=True, verbose_name='Is Active')),
                ('is_deleted', models.BooleanField(blank=True, default=False, null=True, verbose_name='Is Deleted')),
                ('deleted', models.DateTimeField(blank=True, null=True, verbose_name='Deleted')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('file', models.FileField(upload_to=community.apps.community_medias.models.index.file_path, verbose_name='File')),
                ('url', models.URLField(blank=True, null=True, verbose_name='URL')),
                ('media_type', models.CharField(blank=True, choices=[('BANNER', 'BANNER')], max_length=100, null=True, verbose_name='Media Type')),
                ('file_type', models.CharField(blank=True, choices=[('IMAGE', 'IMAGE'), ('VIDEO', 'VIDEO')], max_length=100, null=True, verbose_name='File Type')),
                ('order', models.IntegerField(default=1, verbose_name='Order')),
                ('community', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='community_medias', to='communities.community', verbose_name='Community')),
            ],
            options={
                'verbose_name': 'Community Media',
                'verbose_name_plural': 'Community Media',
                'ordering': ['order'],
            },
            bases=(community.bases.models.UpdateMixin, models.Model),
        ),
    ]
