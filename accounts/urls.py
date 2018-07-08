from django.urls import path
from django.contrib.auth import views as auth_view
from . import views


login_template = "accounts/login.html"

urlpatterns = [
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('register/', views.register, name="register"),
]