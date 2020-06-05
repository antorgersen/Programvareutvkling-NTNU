from django.db import models
from django.conf import settings


# Create your models here.

class Challenge(models.Model):
    challenge_name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    rec_user_level = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_by')
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='participants',
                                          blank=True)


class KnitNight(models.Model):
    knit_name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    time = models.DateTimeField()
    time_start = models.TimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_by1')
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='participants1',
                                          blank=True)


class Ads(models.Model):
    yarn_name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    url = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_by2')
