Application
===========

Application is where components combies together. First application
define in **clink.Application** class. To create an HTTP APIs, you must
create application.

Every application implement **clink.IWsgi**. It is an WSGI and
allow application run on WSGI server.

Here are steps to create an application:

.. literalinclude:: ../sample/app_creation.py
    :language: python

Now, dick into each steps.

Step 1: Get Clink library
-------------------------

**clink.App**: Built-in application. It's an implementations of Pipe Line and
components model, contains built-in components such as JSON conversion,
logging, etc. It allows to create an HTTP API from configuration,
add other components and ready to run on WSGI server.

**clink.AppConf**: Application configuration.

**clink.com**: An decorator helps you mark an class become
component and specifies it's depedencies.

**clink.route**: An decorator helps you specify routing.

**clink.Controller**: An abstract class, doesn't contains any things, but
it uses to mark an class is component and classify as controller. Then
application knows that is controller, add it to routing.

Step 2: Get WSGI server
-----------------------

Here, we use built-in WSGI server in Python. You can chose other servers.

Step 3: Create application
--------------------------

**clink.AppConf** is an component, however others components may depends
on it, so it MUST provide as a argument of **clink.App** constructor.

Step 4: Define components
-------------------------

This step defines components, it MUST be marked by **clink.com**.

We define an controller, it MUST be extend from **clink.Controller**
to help application get knowledge about it.
**route.path('book')** and **route.get('item')** specifies that:
**BookCtl.get_item** will be call if client perform request
**GET /book/item**.

Step 5: Add components to application
-------------------------------------

Simply, add type of components to application, then application knows
"How to create it?. How to bring them togeter?", etc.

Step 6: Load components
-----------------------

Application creates instance of components, solve depedency of components,
etc. It ensure that everythings are ready to runs.

Step 7: Serve application in WSGI server
----------------------------------------

We create an WSGI server, specify address and port to bind and make it
available on network.

Now you can test it:

.. code-block:: shell-session

    $ python app_creation.py &> /dev/null &
    [1] 5946

    $ curl localhost:8080/book/item
    {"author": "Death", "name": "How to Die"}

    $ kill %1
