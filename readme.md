# CLINK

[![Build Status](https://travis-ci.org/kevin-leptons/clink.svg?branch=master)](https://travis-ci.org/kevin-leptons/clink)

[![Documentation Status](https://readthedocs.org/projects/clink/badge/?version=latest)](http://clink.readthedocs.io/en/latest/?badge=latest)

HTTP APIs framework.

![gwisp logo](asset/logo-64.png)

Kevin Leptons <Kevin.leptons@gmail.com> <br>
CC by 4.0 license <br>
May, 2017 <br>

# FEATURES

- Pipe Line handlers
- Component architecture
- Routing by method, path and content type
- Data flow
- Built-in services and controllers for account management, authentication

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
# STEP 1: get clink library
from clink import stamp, mapper, App, AppConf, Controller


# STEP 2: get an WSGI server
from wsgiref.simple_server import make_server


# STEP 3: create application 
conf = AppConf('book-api')
app = App(conf)


# STEP 4: define controller
@stamp()
@mapper.path('book')
class BookCtl(Controller):
    @mapper.get('item')
    def get_item(self, req, res):
        res.body = {
            'name': 'How to Die',
            'author': 'Death'
        }


# STEP 5: add controller to application
app.add_ctl(BookCtl)


# STEP 6: load components
app.load()


# STEP 7: serve application on WSGI server
address = 'localhost'
port = 8080
print('Prepare API on http://%s:%i/book/item' % (address, port))
httpd = make_server(address, port, app)
httpd.serve_forever()
```

## Check API

```bash
$ python server.py &> /dev/null &
[1] 7564

$ curl localhost:8080/book/item
{"name": "How to Die", "author": "Death"}

$ kill %1
```

# REFERENCES

- [Home Page](https://kevin-leptons.github.io/clink/)
- [Clink document](http://clink.readthedocs.io/en/latest/)
- [API](https://en.wikipedia.org/wiki/Application_programming_interface)
- [Web API](https://en.wikipedia.org/wiki/Web_API)
- [MongoDB](https://en.wikipedia.org/wiki/MongoDB)
- [JSON](https://en.wikipedia.org/wiki/JSON)
