# CLINK

[![Build Status](https://travis-ci.org/kevin-leptons/clink.svg?branch=master)](https://travis-ci.org/kevin-leptons/clink)

HTTP APIs framework.

![gwisp logo](asset/logo-64.png)

Kevin Leptons <Kevin.leptons@gmail.com> <br>
CC by 4.0 license <br>
May, 2017 <br>

# FEATURES

- Routing by method, path and content type
- Process follow a pipe with handlers
- Handlers for logging
- Handlers for common data such as JSON, URL ENCONDE
- Utilities to decorate with handlers
- Work flow with database
- *Work flow with OAuth2: Processing*

# USAGE

## Installation

```bash
# python3 is use as interpreter for python language
# curl use to test api
apt-get install python3 wget curl

# pip is python package manager
wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py

# install clink through pip
pip install clink

```

## Create API

Create an file called **server.py** below:

```python
from wsgiref.simple_server import make_server
from clink import Application
from clink.routing import Route, Router

ADDRESS = 'localhost'
PORT = 8080

# create route
book_route = Route('book')


# add request handle to route
@book_route.get('item')
def get_book(req, res):
    res.body = {
        'name': 'Linux Programming Interface',
        'author': 'Michael Kerrisk'
    }


# create application
router = Router([book_route])
app = Application('book-api', router)

# serve application
print('Prepare to start on http://%s:%i' % (ADDRESS, PORT))
httpd = make_server(ADDRESS, PORT, app)
httpd.serve_forever()
```

## Test API

```bash
$ # start server in background
$ python server.py &> /dev/null &

$ # test api
$ curl localhost:8080/book/item
{"name": "Linux Programming Interface", "author": "Michael Kerrisk"}

$ # stop api
$ kill %1
```

# REFERENCES

- [Clink document](http://clink.readthedocs.io/en/latest/)
- [API](https://en.wikipedia.org/wiki/Application_programming_interface)
- [Web API](https://en.wikipedia.org/wiki/Web_API)
- [MongoDB](https://en.wikipedia.org/wiki/MongoDB)
- [JSON](https://en.wikipedia.org/wiki/JSON)
