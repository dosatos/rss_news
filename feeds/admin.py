from django.contrib import admin
from feeds.models import Source, Article


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'link')


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'link')