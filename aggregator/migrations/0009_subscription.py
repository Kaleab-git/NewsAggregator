# Generated by Django 5.0.1 on 2024-01-23 08:04

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aggregator', '0008_alter_news_pub_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.CharField(max_length=255)),
                ('subscribers', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=15), size=None)),
            ],
        ),
    ]