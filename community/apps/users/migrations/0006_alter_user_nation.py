# Generated by Django 3.2.16 on 2024-05-10 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_user_admin_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='nation',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Nation'),
        ),
    ]
