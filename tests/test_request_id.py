# -*- coding:utf-8 -*-

"""Tests for request-id middleware (Flask and Quart)."""

import asyncio
import flask
import quart
from flask import request as flask_request
from quart import request as quart_request
from request_id import RequestId
import unittest
import uuid


class RequestIdTestCase(unittest.TestCase):

    def setUp(self):
        self.header_name = 'X-Request-ID'

        # Flask setup
        self.flask_app = flask.Flask(__name__)

        @self.flask_app.route('/')
        def flask_index():
            request_id = flask_request.environ.get('REQUEST_ID', '')
            return str(request_id)

        RequestId(self.flask_app)

        # Quart setup
        self.quart_app = quart.Quart(__name__)

        @self.quart_app.route('/')
        async def quart_index():
            request_id = quart_request.scope.get('request_id', '')
            return str(request_id)

        RequestId(self.quart_app)

    def test_flask_header_returned(self):
        with self.flask_app.test_client() as c:
            r = c.get('/', headers={self.header_name: '123'})
            self.assertIn(self.header_name, r.headers)

    def test_flask_id_returned(self):
        with self.flask_app.test_client() as c:
            r = c.get('/', headers={self.header_name: '123'})
            self.assertEqual('123', r.headers.get(self.header_name))

    def test_flask_generated_header(self):
        with self.flask_app.test_client() as c:
            r = c.get('/')
            self.assertIn(self.header_name, r.headers)

    def test_flask_generated_id(self):
        with self.flask_app.test_client() as c:
            r = c.get('/')
            self.assertTrue(
                uuid.UUID(r.headers.get(self.header_name), version=4))

    def test_flask_id_in_environ(self):
        with self.flask_app.test_client() as c:
            r = c.get('/', headers={self.header_name: '123'})
            self.assertEqual('123', r.get_data(as_text=True))

    def test_quart_header_returned(self):
        async def run_test():
            async with self.quart_app.test_client() as c:
                r = await c.get('/', headers={self.header_name: '123'})
                self.assertIn(self.header_name, r.headers)
        asyncio.run(run_test())

    def test_quart_id_returned(self):
        async def run_test():
            async with self.quart_app.test_client() as c:
                r = await c.get('/', headers={self.header_name: '123'})
                self.assertEqual('123', r.headers.get(self.header_name))
        asyncio.run(run_test())

    def test_quart_generated_header(self):
        async def run_test():
            async with self.quart_app.test_client() as c:
                r = await c.get('/')
                self.assertIn(self.header_name, r.headers)
        asyncio.run(run_test())

    def test_quart_generated_id(self):
        async def run_test():
            async with self.quart_app.test_client() as c:
                r = await c.get('/')
                self.assertTrue(
                    uuid.UUID(r.headers.get(self.header_name), version=4))
        asyncio.run(run_test())

    def test_quart_id_in_scope(self):
        async def run_test():
            async with self.quart_app.test_client() as c:
                r = await c.get('/', headers={self.header_name: '123'})
                self.assertEqual('123', await r.get_data(as_text=True))
        asyncio.run(run_test())


if __name__ == '__main__':
    unittest.main()
