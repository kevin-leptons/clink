Quickstart
==========

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

.. literalinclude:: ../sample/app_creation.py
    :language: python

Testing
-------

.. code-block:: shell-session

    $ python server.py &> /dev/null &
    [1] 10297

    $ curl localhost:8080/book/item
    {"name": "Linux Programming Interface", "author": "Michael Kerrisk"}

    $ kill %1
