# Generated by Django 3.2.16 on 2024-07-30 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_set_passwords'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='religion',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='Religion'),
        ),
    ]