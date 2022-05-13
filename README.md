# request-id-flask

Attach a unique identifier to every HTTP request in your WSGI application.

`request-id-flask` is implemented as a WSGI middleware.

The package will do one of two things:

1. Read the `X-Request-ID` HTTP header from a client HTTP request and return the **same** `X-Request-ID` HTTP header in the server HTTP response and is stored in the WSGI `environ`.

2. Or, when no `X-Request-ID` HTTP header is present in the client HTTP request, generate a new and unique `request_id` identifier (using uuid 4) which is stored in the WSGI `environ` and set as the `X-Request-ID` HTTP header in the server HTTP responser.


## Requirements

- Python 3.6 or above


## Installation

You can install the request-id-flask package using pip:

```shell
pip install flask-ext-request-id
```

However, recommended to add it to the `requirements.txt` file instead.

## Access the request_id

The `REQUEST_ID` is stored in the request `environ` dictionary and may be accessed from anywhere this is available in Flask.


## Usage

```python
from flask import (
    Flask,
    request
)
from request_id import RequestId

app = Flask(__name__)
RequestId(app)


@app.route('/')
def index():
    request_id = request.environ.get('REQUEST_ID', '')
    return str(request_id)
```
