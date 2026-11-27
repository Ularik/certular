import json
from unittest.mock import patch

from django.test import RequestFactory, SimpleTestCase

from .views import login_view


class LoginViewTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_rejects_non_post_requests(self):
        response = login_view(self.factory.get('/accounts/login/'))

        self.assertEqual(response.status_code, 405)

    def test_rejects_malformed_json(self):
        request = self.factory.generic(
            'POST',
            '/accounts/login/',
            data=b'{',
            content_type='application/json',
        )

        response = login_view(request)

        self.assertEqual(response.status_code, 400)

    def test_rejects_missing_credentials(self):
        request = self.factory.post(
            '/accounts/login/',
            data=json.dumps({'username': 'person@example.com'}),
            content_type='application/json',
        )

        response = login_view(request)

        self.assertEqual(response.status_code, 400)

    @patch('accounts_app.views.authenticate', return_value=None)
    def test_accepts_form_encoded_login_data(self, authenticate):
        request = self.factory.post(
            '/accounts/login/',
            data={'username': 'person@example.com', 'password': 'wrong-password'},
        )

        response = login_view(request)

        self.assertEqual(response.status_code, 401)
        authenticate.assert_called_once()


from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Organization, User


@override_settings(LANGUAGE_CODE='ru')
class AdminUserCreateTests(TestCase):
    def setUp(self):
        patcher = patch('accounts_app.signals.requests.get')
        self.telegram_get = patcher.start()
        self.addCleanup(patcher.stop)
        self.admin = User.objects.create_user(
            email='admin@example.com', first_name='Admin', password='Adm1n-pass!', is_admin=True,
        )
        self.client.force_login(self.admin)
        self.org = Organization.objects.create(name='Тестовая организация', org_code='TST')
        self.url = reverse('admin:accounts_app_user_add')

    def test_add_form_renders_with_phone_placeholder(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'placeholder="+996 (555) 12-34-56"')

    def test_create_user_via_admin(self):
        response = self.client.post(self.url, {
            'email': 'new@example.com',
            'first_name': 'Иван',
            'password1': 'Str0ng-passw0rd!',
            'password2': 'Str0ng-passw0rd!',
            'usable_password': 'true',
            'organization': self.org.pk,
            'number': '+996 (555) 12-34-56',
        })
        self.assertEqual(response.status_code, 302, getattr(response, 'context', None) and
                         response.context['adminform'].form.errors)
        user = User.objects.get(email='new@example.com')
        self.assertTrue(user.check_password('Str0ng-passw0rd!'))
        self.assertEqual(user.organization, self.org)
        self.assertEqual(user.number, '+996 (555) 12-34-56')

    def test_rejects_invalid_phone(self):
        response = self.client.post(self.url, {
            'email': 'bad@example.com',
            'first_name': 'Иван',
            'password1': 'Str0ng-passw0rd!',
            'password2': 'Str0ng-passw0rd!',
            'usable_password': 'true',
            'number': 'abc',
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('number', response.context['adminform'].form.errors)
        self.assertFalse(User.objects.filter(email='bad@example.com').exists())

    def test_change_form_has_phone_placeholder(self):
        response = self.client.get(reverse('admin:accounts_app_user_change', args=[self.admin.pk]))
        self.assertContains(response, 'placeholder="+996 (555) 12-34-56"')

    def test_telegram_failure_does_not_break_creation(self):
        import requests
        self.telegram_get.reset_mock()
        self.telegram_get.side_effect = requests.ConnectionError('down')
        with patch.dict('os.environ', {'TELEGRAM_API': 'https://api.example', 'TELEGRAM_CHAT_ID': '1'}):
            User.objects.create_user(email='tg@example.com', first_name='T', password='x', number='+996555123456')
        self.assertTrue(User.objects.filter(email='tg@example.com').exists())
        self.telegram_get.assert_called_once()

    def test_create_admin_user_via_admin(self):
        response = self.client.post(self.url, {
            'email': 'staff@example.com',
            'first_name': 'Пётр',
            'password1': 'Str0ng-passw0rd!',
            'password2': 'Str0ng-passw0rd!',
            'usable_password': 'true',
            'is_admin': 'on',
            'number': '+996 (555) 12-34-56',
        })
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(email='staff@example.com')
        self.assertTrue(user.is_admin)
        self.assertTrue(user.is_staff)
