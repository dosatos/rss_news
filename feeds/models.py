from django.db import models


class Source(models.Model):
    id = models.IntegerField(primary_key=True, null=False, blank=False)
    title = models.CharField(max_length=100, null=False, blank=False)
    link = models.CharField(max_length=100, null=False, blank=False)
    date_added = models.DateTimeField(auto_now_add=True)
