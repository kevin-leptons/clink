Components
==========

For now, Clink is design follow Pipe Line Model, that mean
handlers had format look like below:

.. code-block:: python

    def handle(req, res, ...):
        pass

However, handler need to shares, accesses shared resources such as
database connection, configurations, etc. We avoid to do it though
function's arguments because each time invoke handler, we MUST detect
what is resources handler required, where is it, etc. In simple, it
take down performance and take up complicated.

Awesome solution is **Components**. **Components** is concept includes
component, auto creation, depedency solving, and get instances. All of
that concept be perform by **Injector**. For example:

.. literalinclude:: ../example/usage/components.py
    :language: python
    :caption: components.py:

Test it
-------

.. code-block:: shell-session

    $ python components.py
    created: {'name': 'Micheal', 'email': 'michael@mars.com'}
    <__main__.AccountService object at 0x7f4716069f28>

Component
---------

Component is wrapped context. It puts all of references to dependencies
and component's functions together. So functions can accesses quickly
to dependencies.

**@com(AccountService)** specify that AccountCtl depends on AccountService.

AccountCtl extend from **Component** to mark that AccountCtl is an component.
However, Component doesn't contains any things.

Auto Creation
-------------

Because Component is class, it MUST be create to run. It's perform
automatically by injector. With abow example, during auto creation,
an instance of AccountService will pass into first param of
AccountCtl.__init__() without handle from developers.

Depedency Solving
-----------------

**@com** decorator specify dependencies. During auto creation, dependencies
of component will be recursive analyst, create automatically. That is
reason why we don't add **AccountService** component but we still can
get an instance of it.

Get Instances
-------------

Access instance of component by type.
