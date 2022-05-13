# -*- coding: utf-8 -*-

import uuid


class RequestId(object):
    """Middleware to capture request header from incoming http request
    """

    def __init__(self, app=None):
        # Load configuration
        if app is not None:
            self.init_app(app)
        # Define header names
        self._header = app.config.get('REQUEST_ID_HEADER_NAME')
        # Set wsgi
        self.app = app.wsgi_app
        app.wsgi_app = self

    def init_app(self, app):
        # Set configuration
        app.config.setdefault(
            'REQUEST_ID_HEADER_NAME',
            'X-Request-ID'
        )

    def __call__(self, environ, start_response):
        # Reading request headers
        request_id = environ.get(
            f'HTTP_{self._header}'.replace('-', '_').upper(),
            None
        )
        if request_id is None:
            request_id = str(uuid.uuid4())
        # Define the new header
        environ.setdefault('REQUEST_ID', request_id)

        def new_start_response(status, response_headers, exc_info=None):
            # Add the new header to the response
            response_headers.append((self._header, request_id))
            return start_response(status, response_headers, exc_info)

        return self.app(environ, new_start_response)
