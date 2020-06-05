from django.db import models

from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver


# Creating our post model
class Personal_Feed_Post(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False)
    content = models.TextField(max_length=5000, null=False, blank=False)
    date_published = models.DateTimeField(auto_now_add=True, verbose_name='date published')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # In case you haven't seen this, a slug is just a URL, we have to make sure each URL is unique
    slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.title

# Here, we're going to ensure that we have a unique link in the form we choose


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.author.username + "-" + instance.title)


pre_save.connect(pre_save_post_receiver, sender=Personal_Feed_Post)
