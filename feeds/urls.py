from django.urls import path
from . import views

urlpatterns = [
    path('/', views.feeds, name='feeds'),
    path('/sources', views.sources, name='sources'),
]