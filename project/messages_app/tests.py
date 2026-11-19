import threading
from email.parser import BytesParser
from email.policy import HTTP
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from types import SimpleNamespace
from unittest import mock

from django.core.files.base import ContentFile
from django.test import SimpleTestCase, override_settings

from messages_app import forwarding


def make_message(file=None):
    return SimpleNamespace(
        pk=7, user=None, email='a@b.kg', name='Иванов Иван', phone_number='+996555123456',
        description='Взломали сайт, см. http://x.kg', host_ip='1.2.3.4', domain_name='x.kg',
        hash='abc', file=file, created_at=datetime(2026, 11, 19, tzinfo=timezone.utc),
    )


class FakeFieldFile:
    """Минимальная замена FieldFile: имя + open()."""

    def __init__(self, name, content):
        self.name = name
        self._content = content

    def __bool__(self):
        return True

    def open(self, mode='rb'):
        return ContentFile(self._content)


class ForwardMessageTests(SimpleTestCase):

    @override_settings(MESSAGE_SEND_ADDRESS='')
    def test_no_address_does_nothing(self):
        with mock.patch.object(forwarding.threading, 'Thread') as thread:
            forwarding.forward_message(make_message())
        thread.assert_not_called()

    @override_settings(MESSAGE_SEND_ADDRESS='http://example.test/hook')
    def test_address_starts_background_send(self):
        message = make_message()
        with mock.patch.object(forwarding.threading, 'Thread') as thread:
            forwarding.forward_message(message)
        thread.assert_called_once_with(
            target=forwarding.send_message_to_address,
            args=(message, 'http://example.test/hook'), daemon=True,
        )
        thread.return_value.start.assert_called_once()

    def test_network_error_is_logged_not_raised(self):
        with mock.patch.object(forwarding.requests, 'post', side_effect=forwarding.requests.ConnectionError):
            with self.assertLogs('messages_app.forwarding', level='ERROR'):
                self.assertFalse(forwarding.send_message_to_address(make_message(), 'http://example.test/'))

    def test_posts_multipart_with_file_to_real_server(self):
        received = {}

        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):
                body = self.rfile.read(int(self.headers['Content-Length']))
                msg = BytesParser(policy=HTTP).parsebytes(
                    b'Content-Type: ' + self.headers['Content-Type'].encode() + b'\r\n\r\n' + body)
                received['fields'] = {}
                for part in msg.iter_parts():
                    name = part.get_param('name', header='content-disposition')
                    payload = part.get_payload(decode=True)
                    if name == 'file':
                        received['file'] = (part.get_filename(), payload)
                    else:
                        received['fields'][name] = payload.decode('utf-8')
                self.send_response(200)
                self.end_headers()

            def log_message(self, *args):
                pass

        server = HTTPServer(('127.0.0.1', 0), Handler)
        t = threading.Thread(target=server.handle_request, daemon=True)
        t.start()
        try:
            url = f'http://127.0.0.1:{server.server_port}/hook'
            message = make_message(file=FakeFieldFile('Messages/2026-11-19/log.txt', b'payload'))
            with mock.patch.object(forwarding, 'logger'):  # db_logger пишет в БД, а здесь её нет
                self.assertTrue(forwarding.send_message_to_address(message, url))
        finally:
            t.join(5)
            server.server_close()

        fields = received['fields']
        self.assertEqual(fields['id'], '7')
        self.assertEqual(fields['email'], 'a@b.kg')
        self.assertEqual(fields['description'], 'Взломали сайт, см. http://x.kg')
        self.assertEqual(fields['full_name'], 'Иванов Иван')
        self.assertEqual(fields['host_ip'], '1.2.3.4')
        self.assertEqual(received['file'], ('log.txt', b'payload'))
