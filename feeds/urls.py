from django.urls import path
from . import views

urlpatterns = [
    path('', views.feeds, name='feeds'),
    path('sources/', views.source_page, name='sources'),
    path('add-bookmark/', views.add_bookmark, name='add-bookmark'),
    path('bookmarks/', views.bookmarks, name='bookmarks'),
]