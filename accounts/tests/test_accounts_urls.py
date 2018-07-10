from django.urls import reverse, resolve


def test_login_url_exists():
    path = reverse('login')
    assert resolve(path).view_name == 'login'


def test_logout_url_exists():
    path = reverse('logout')
    assert resolve(path).view_name == 'logout'


def test_register_url_exists():
    path = reverse('register')
    assert resolve(path).view_name == 'register'
