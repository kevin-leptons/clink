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
    name=kevin, password=secret-words, validated
    FormatError: name=name, value=ke vin, schema={'pattern': 
    '^[a-z0-9-]{2,32}$', 'type': 'string'}
