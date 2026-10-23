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
