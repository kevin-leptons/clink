Quick start
===========

Installation
------------

.. code-block:: bash

    # python3 is use as interpreter for python language
    # curl use to test api
    apt-get install python3 wget curl

    # pip is python package manager
    wget https://bootstrap.pypa.io/get-pip.py
    python get-pip.py

    # install clink through pip
    pip install clink

Writting
--------

Create an file named **server.py** below:

.. literalinclude:: ../sample/simple_server.py
    :language: python

Testing
-------

.. code-block:: shell-session

    $ # start api in background
    $ python server.py &
    Prepare to start on http://localhost:8080

    $ # test it
    $ curl localhost:8080/book/item
    {"name": "Linux Programming Interface", "author": "Michael Kerrisk"}
