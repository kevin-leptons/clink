verify()
========

.. autofunction:: clink.dflow.verify.verify


Example
-------

.. literalinclude:: ../example/api/dflow_verify.py
    :language: python
    :caption: dflow_verify.py

Testing
-------

.. code-block:: shell-session

    $ python dflow_verify.py
    Car is running on the 1st Hell Street
    Error:  name=, value=1st Hell Street @@@, schema={'pattern': 
    '^[a-zA-Z0-9 ]{6,32}$', 'type': 'string'}
