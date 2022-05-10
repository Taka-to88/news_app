# from email.mime import image
from django.db import models

# Create your models here.


class News(models.Model):
    title = models.CharField(max_length=100)
    link = models.URLField(null=True)
    published = models.DateTimeField()
    image = models.ImageField(upload_to='media/', null=True)
    body = models.TextField()

    def __str__(self):
        return self.title

    def summary(self):
        return self.body[:60]+'...'
