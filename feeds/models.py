from django.db import models


class Source(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    link = models.CharField(max_length=100, null=False, blank=False, unique=True)
    date_added = models.DateTimeField(auto_now_add=True)


class Article(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    body = models.TextField(max_length=1000, null=False, blank=False)
    link = models.CharField(max_length=255, null=False, blank=False, unique=True)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    date_published = models.DateTimeField(null=True)
    date_added = models.DateTimeField(auto_now_add=True)