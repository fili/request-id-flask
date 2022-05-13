#-*- coding:utf-8 -*-

"""Tests for request-id-flask."""

import flask
from request_id import RequestId
import unittest
import uuid


class RequestIdTestCase(unittest.TestCase):

    def setUp(self):
        self.app = flask.Flask(__name__)

        @self.app.route('/')
        def index():
            return 'Hello, World'

        RequestId(self.app)
        self.header_name = 'X-Request-ID'

    def test_header_returned(self):
        with self.app.test_client() as c:
            r = c.get('/', headers={
                self.header_name: '123'
            })
            self.assertTrue(
                bool(self.header_name in list(r.headers.keys()))
            )

    def test_id_returned(self):
        with self.app.test_client() as c:
            r = c.get('/', headers={
                self.header_name: '123'
            })
            self.assertEqual(
                '123',
                r.headers.get(self.header_name)
            )

    def test_generated_header(self):
        with self.app.test_client() as c:
            r = c.get('/')
            self.assertTrue(
                bool(self.header_name in list(r.headers.keys()))
            )

    def test_generated_id(self):
        with self.app.test_client() as c:
            r = c.get('/')
            self.assertTrue(
                bool(
                    uuid.UUID(
                        r.headers.get(self.header_name), version=4
                    )
                )
            )
