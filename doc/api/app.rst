App
===

.. autoclass:: clink.App
    :special-members: __call__
    

.. _api-app-example:

Example
-------

.. literalinclude:: ../example/api/app.py
    :language: python
    :caption: app.py

Testing
-------

.. code-block:: shell-session

    $ python app.py
    [1] 5940

    $ curl localhost:8080/book/item
    {"name": "How to Die", "author": "Death"}

    $ kill %1
