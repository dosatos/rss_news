from django.urls import reverse, resolve


class TestUrls:

    def test_login_url_exists(self):
        path = reverse('login')
        assert resolve(path).view_name == 'login'

    def test_logout_url_exists(self):
        path = reverse('logout')
        assert resolve(path).view_name == 'logout'

    def test_register_url_exists(self):
        path = reverse('register')
        assert resolve(path).view_name == 'register'
