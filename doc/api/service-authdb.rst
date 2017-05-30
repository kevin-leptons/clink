AuthDbSv
========

.. autoclass:: clink.service.AuthDbSv

Example
-------

.. literalinclude:: ../sample/api/authdb_sv.py
    :language: python

Testing
-------

.. code-block:: shell-session

    $ python authdb_sv.py
    <class 'pymongo.collection.Collection'> account
    <class 'pymongo.collection.Collection'> group
    <class 'pymongo.collection.Collection'> rpwd
    <class 'pymongo.collection.Collection'> acctmp
