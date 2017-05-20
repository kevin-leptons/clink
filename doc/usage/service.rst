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

Clink also provides built-in service, check it out in **API - Services**.

Now, let create an service, share way to public newsparer or magazine.
It accepts type and content of newsparer, magazine then generate string
includes information of application with type and content. Two controllers
use this service though injector.

Go back **app_creation** then modify program to get code below:

.. literalinclude:: ../sample/app_service.py
    :language: python

Test it:

.. code-block:: shell-session

    $ python app_service.py &> /dev/null &
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
    Id: 592050fae7798916e88e93f9
    Type: MAGAZINE
    Content:

    This is awesome magazine

    book-api
    Hell Corporation
    1st, Hell street

    $ kill %1
