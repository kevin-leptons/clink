Routing
=======

Clink's routing is simple but efficiency. It not allow parameters in
path for explicit and performance. Let use query arguments instead of
path parameters. For examples:

.. table::

    =============================== ==========================================
    Parameter form                  Argument form
    =============================== ==========================================
    /book/:id                       /book/item?id=1243
    /book/:id/notes                 /book/item/notes?id=1243
    /news/:year/:month/:date        /news/archive?year=2017&month=5&date=3
    =============================== ==========================================

However, arguments isn't introduce here, it's introduce in **Controller**
section.

Clink's routing provides routing methods by three factors: **method**,
**path**, **content-type**. All of it can be done with **clink.route**.

- clink.route.get(path)
- clink.route.post(path, type=MIME_JSON)
- clink.route.put(path, type=MIME_JSON)
- clink.route.patch(path, type=MIME_JSON)
- clink.route.delete(path)

As you see, GET and DELETE method ignores content-type because it's no
meaning. Other methods allow content-type with default value is MIME_JSON.
You can access shortcut name for MIME type in **clink.mime.type**.

Now, modify **app_creation**  to get knowledge about routing:

.. literalinclude:: ../sample/app_routing.py
    :language: python

Test it:

.. code-block:: shell-session

    $ python app_routing.py &> /dev/null &
    [1] 7071

    $ curl -X GET localhost:8080/book/item; echo
    {"name": "How to Die", "author": "Death"}

    $ curl -X POST -H "Content-Type: text/plain" localhost:8080/book/item; \
      echo
    {"msg": "created"}

    $ curl -X POST -H "Content-Type: application/json" \
      localhost:8080/book/item; echo
    {"status_name": "406 Not Accepted", "message": null, "status": 406}

    $ curl localhost:8080/not-exist-path; echo
    {"status_name": "404 Not Found", "message": null, "status": 404}
