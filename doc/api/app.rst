App
===

.. autoclass:: clink.App
    

**Example**

.. literalinclude:: ../sample/api/app.py
    :language: python

**Testing**

.. code-block:: shell-session

    $ python app.py
    [1] 5940

    $ curl localhost:8080/book/item
    {"name": "How to Die", "author": "Death"}
