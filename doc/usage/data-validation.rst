Data Validation
===============

Data validation use many CPU resource, any mistake on data validation will 
down system into hole. Clink provides a mechanism to controll all of this 
processing in :ref:`api-dflow`. In simple, put one data validation in
service.

Example
-------

.. literalinclude:: ../example/usage/data_validation.py
    :language: python
    :caption: data_validation.py

Testing
-------

.. code-block:: shell-session

    $ python data_validation.py &> /dev/null &
    [1] 9977

    $ curl -X POST -H "Content-Type: application/json" \
    -d '{"name": "Dead Note"}' localhost:8080/book/item; echo
    {"message": {"value": "{'name': 'Dead Note'}", "name": "book", 
    "schema": {"type": "object", "properties": {"name": {"type": 
    "string", "pattern": "^[a-zA-Z0-9 ]{2,32}$"}, "author": {"type": 
    "string", "pattern": "^[a-zA-Z0-9 ]{2,16}$"}}, "required": 
    ["name", "author"], "additionalProperties": false}}, 
    "status_name": "400 Bad Request", "status": 400}


    $ curl -X POST -H "Content-Type: application/json" \
    -d '{"name": "Dead Note", "author": "Death"}' \
    localhost:8080/book/item; echo
    {"message": "created"}

    $ kill %1
