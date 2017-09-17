Service
=======

Service is component. You should use service when you need:

- Carry big logic processing. Entry of main logic proccessing is handlers
  of controllers, when it too long, you should move it into services.

- Reuse logic processing. May be some handlers must do same of logic
  processing, that borrow to write again and again, best way is services.
  That mean code is more easy to read, debug and maintain.

- Access to shared resources. Shared resources is configurations, connection
  to database, it's some things only exist during runtime. Service is most
  simple way to to do it because serivce is component and Injector give it's
  dependencies automatically.

Clink also provides built-in services, check it out in 
:ref:`api-service`

Example
-------

Now, let create an service, share way to public newsparer or magazine.
It accepts type and content of newsparer, magazine then generate string
includes information of application with type and content. Two controllers
use this service though injector.

.. literalinclude:: ../example/usage/service.py
    :language: python
    :caption: service.py

Testing
-------

.. code-block:: shell-session

    $ python service.py &> /dev/null &
    [1] 5864

    $ curl -X POST -H "Content-Type: text/plain" \
      -d "This is awesome newsparer" localhost:8080/newsparer; echo
    Id: 5920522fe7798916e88e93fd
    Type: NEWSPAPER
    Content:

    This is awesome newsparer

    book-api
    Hell Corporation
    1st, Hell street

    $ curl -X POST -H "Content-Type: text/plain" \
      -d "This is awesome magazine" localhost:8080/magazine; echo
    Id: 59be3309e779894758b26f86
    Type: NEWSPAPER
    Content:

    This is awesome newsparer

    book-api v0.1.0
    Hell Corporation
    1st, Hell street

    $ kill %1
