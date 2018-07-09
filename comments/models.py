from django.db import models
from accounts.models import CustomUser
from feeds.models import Article

class Comment(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.TextField(max_length=140, null=False, blank=False)
    date_added = models.DateTimeField(auto_now_add=True)
