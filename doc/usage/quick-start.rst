Quickstart
==========

Installation
------------

.. code-block:: shell-session

    # python3 is use as interpreter for python language
    # curl use to test api
    $ apt-get install python3 wget curl

    # pip is python package manager
    $ wget https://bootstrap.pypa.io/get-pip.py
    $ python get-pip.py

    # install clink through pip
    $ pip install clink

Writting
--------

.. literalinclude:: ../example/usage/app.py
    :language: python
    :caption: app.py

Testing
-------

.. code-block:: shell-session

    $ python app.py &> /dev/null &
    [1] 10297

    $ curl localhost:8080/book/item
    {"name": "Linux Programming Interface", "author": "Michael Kerrisk"}

    $ kill %1
