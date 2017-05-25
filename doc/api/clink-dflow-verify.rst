verify()
========

.. autofunction:: clink.dflow.verify.verify


Example
-------

.. literalinclude:: ../sample/api/dflow_verify.py
    :language: python

Testing
-------

.. code-block:: shell-session

    $ python dflow_verify.py
    Car is running on the 1st Hell Street
    Error:  name=, value=1st Hell Street @@@, schema={'pattern': 
    '^[a-zA-Z0-9 ]{6,32}$', 'type': 'string'}
