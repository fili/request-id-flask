# -*- coding: utf-8 -*-
import uuid
from functools import wraps


class RequestId:
    """Middleware to capture request header from incoming http request for both Flask and Quart"""

    def __init__(self, app=None):
        self.app = None
        # Load configuration
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        # Set configuration
        app.config.setdefault('REQUEST_ID_HEADER_NAME', 'X-Request-ID')
        # Define header names
        self._header = app.config.get('REQUEST_ID_HEADER_NAME')

        if hasattr(app, 'asgi_app'):  # Quart
            app.asgi_app = self.asgi_middleware(app.asgi_app)
        else:  # Flask
            self.app = app.wsgi_app
            app.wsgi_app = self

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

    def asgi_middleware(self, app):
        @wraps(app)
        async def middleware(scope, receive, send):
            if scope['type'] == 'http':
                request_id = None
                for name, value in scope['headers']:
                    if name.decode('utf-8').lower() == self._header.lower():
                        request_id = value.decode('utf-8')
                        break

                if request_id is None:
                    request_id = str(uuid.uuid4())

                scope['request_id'] = request_id

                async def send_wrapper(message):
                    if message['type'] == 'http.response.start':
                        headers = message.get('headers', [])
                        headers.append((self._header.encode(
                            'utf-8'), request_id.encode('utf-8')))
                        message['headers'] = headers
                    await send(message)

                await app(scope, receive, send_wrapper)
            else:
                await app(scope, receive, send)

        return middleware
