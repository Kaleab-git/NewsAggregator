# Generated by Django 5.0.1 on 2024-01-18 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aggregator', '0007_alter_news_link_alter_news_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='pub_date',
            field=models.DateTimeField(),
        ),
    ]