from unittest.mock import patch
from io import StringIO

import tornado.web
import tornado.gen
import tornado.httpclient
import tornado.testing

import example.server


class TestAppTornadoStyle(tornado.testing.AsyncHTTPTestCase):

    def setUp(self):
        super(TestAppTornadoStyle, self).setUp()
        self.real_async_client = tornado.httpclient.AsyncHTTPClient(
            self.io_loop)
        self.async_patcher = patch('tornado.httpclient.AsyncHTTPClient')
        self.mock_async_client = self.async_patcher.start()

    def tearDown(self):
        self.async_patcher.stop()

    def get_app(self):
        self.errors = example.server.get_errors()
        return example.server.initialise()

    def test_no_url_sent(self):
        self.real_async_client.fetch(
            self.get_url('/'), self.stop)
        response = self.wait()

        assert response.code == 400
        assert self.errors['missing'] in str(response.body)

    def test_invalid_url_sent(self):
        self.real_async_client.fetch(
            self.get_url('/?url=google'), self.stop)
        response = self.wait()

        assert response.code == 400
        assert self.errors['invalid'] in str(response.body)

    def test_asynchttpclient(self):
        request = tornado.httpclient.HTTPRequest('http://google.com')
        response = tornado.httpclient.HTTPResponse(
            request, 200, buffer=StringIO('google'))
        self.mock_async_client().fetch.side_effect = lambda x, y: y(response)
        self.real_async_client.fetch(
            self.get_url('/?url=http://google.com'), self.stop)
        response = self.wait()
        assert response.code == 200
        assert 'google' in str(response.body)
