#-*- coding:utf-8 -*-

"""Tests for request-id-flask."""

import flask
from flask import request
from request_id import RequestId
import unittest
import uuid


class RequestIdTestCase(unittest.TestCase):

    def setUp(self):
        self.app = flask.Flask(__name__)
        self.header_name = 'X-Request-ID'

        @self.app.route('/')
        def index():
            request_id = request.environ.get('REQUEST_ID', '')
            return str(request_id)

        RequestId(self.app)

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

    def test_id_in_environ(self):
        with self.app.test_client() as c:
            r = c.get('/', headers={
                self.header_name: '123'
            })
            self.assertEqual(
                '123',
                r.get_data(as_text=True)
            )
