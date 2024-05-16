# Generated by Django 5.0.1 on 2024-01-29 12:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aggregator', '0012_delete_subscription'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frequency', models.CharField(choices=[('immediately', 'Immediately'), ('once_a_day', 'Once a Day'), ('twice_a_day', 'Twice a Day'), ('once_a_week', 'Once a Week')], default='immediately', max_length=20)),
                ('email', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='aggregator.email')),
                ('keyword', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aggregator.keyword')),
            ],
            options={
                'unique_together': {('email', 'keyword')},
            },
        ),
    ]
