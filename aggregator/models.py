from django.db import models
from django.contrib.postgres.fields import ArrayField


class News(models.Model):
    title = models.TextField()
    description = models.TextField()
    content = models.TextField()
    pub_date = models.DateTimeField()
    source = models.TextField()
    link = models.TextField()
    thumbnail = models.TextField()
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Subscription(models.Model):
    keyword = models.CharField(max_length=255)
    subscribers = ArrayField(
        models.CharField(max_length=50, blank=True),
        default=list,
    )

    def __str__(self):
        return self.keyword


class Schedule(models.Model):
    FREQUENCY_CHOICES = [
        ('immediately', 'Immediately'),
        ('once_a_day', 'Once a Day'),
        ('twice_a_day', 'Twice a Day'),
        ('once_a_week', 'Once a Week'),
    ]

    email = models.EmailField()
    keyword = models.CharField(max_length=255)
    schedule = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)

    class Meta:
        unique_together = ('email', 'keyword')

    def __str__(self):
        return f'{self.email} - {self.keyword} - {self.schedule}'
