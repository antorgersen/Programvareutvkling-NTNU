from django.db import models


class Inquiries(models.Model):
    text_from = models.CharField(max_length=100, null=True)
    subject = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    created_at = models.DateField(auto_now=True)

    class Meta:
        ordering = ['created_at']


    def __str__(self):
        return '{}/{}'.format(self.subject, self.description)
