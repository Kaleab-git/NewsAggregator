# Generated by Django 5.0.1 on 2024-01-18 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aggregator', '0006_alter_news_source_alter_news_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='link',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='news',
            name='thumbnail',
            field=models.TextField(),
        ),
    ]
