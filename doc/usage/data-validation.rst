Data Validation
===============

Clink provides simple data validation such as JSON schema. 

Now let try it. We create an API accept body as JSON object with two 
properties. **name** is string, contains alpha and numeric, 
length >= 2 and <= 32. **author** is the same, however length <= 16.
Maximum content size is 50 bytes.

.. _usage-data-validation-example:

Example
-------

.. literalinclude:: ../sample/app_data_validation.py
    :language: python

Testing
-------

.. code-block:: shell-session

    $ python app_data_validation.py &> /dev/null &
    [1] 9977

    $ curl -X POST -H "Content-Type: application/json" \
      -d '{"name": "How to Die?", "author": "Death"}' \
      localhost:8080/book/item; echo
    {"status_name": "400 Bad Request", "message": "Invalid body: 
    'How to Die?' does not match '^[a-zA-Z0-9 ]{2,32}$'\n\nFailed validating 
    'pattern' in schema['properties']['name']:\n    
    {'pattern': '^[a-zA-Z0-9 ]{2,32}$', 'type': 'string'}\n\nOn 
    instance['name']:\n    'How to Die?'", "status": 400}

    $ curl -X POST -H "Content-Type: application/json" \
      -d '{"name": "How to Die", "author": "Death", "notes": "long long"}' \
      localhost:8080/book/item; echo
    {"status": 413, "status_name": "413 Request Entity Too Large", 
    "message": null}

    $ curl -X POST -H "Content-Type: application/json" \
      -d '{"name": "How to Die", "author": "Death"}' \
      localhost:8080/book/item; echo
    {"msg": "created"}

    $ kill %1
