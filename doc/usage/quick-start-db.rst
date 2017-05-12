Quickstart Datbase
==================

Use MongoDB.

Writting
--------

Create an file named **db_node.py** below:

.. literalinclude:: ../sample/mongo_node.py
    :language: python

Testing
-------

.. code-block:: shell-session

    $ python db_node.py
    {'name': 'How to Die', '_id': ObjectId('5915c594e779896a7ccd74ae'),
    'author': 'Death'}
