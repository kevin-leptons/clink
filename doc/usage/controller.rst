Controller
==========

You know Controller in before sections, now let access request data
and modify response. Get back to **app_creation**, remove BookCtl and add
RootCtl, we have example below explains how to do it:


Example
-------

.. literalinclude:: ../sample/app_controller.py
    :language: python

Testing
-------

.. code-block:: shell-session

    $ python app_controller.py &> /dev/null &
    [1] 6556

    $ curl -X GET localhost:8080/req/info; echo
    {"query_str": null, "body": null, "header": {"HOST": "localhost:8080",
    "ACCEPT": "*/*", "USER_AGENT": "curl/7.38.0"}, "content_type": null,
    "remote_addr": "127.0.0.1", "server_name": "localhost",
    "server_protocol": "HTTP/1.1", "server_port": 8080, "path": "/req/info",
    "content_length": 0}

    $ curl -X GET -D - localhost:8080/req/no-content; echo
    HTTP/1.0 204 No Content
    Date: Sat, 20 May 2017 14:56:20 GMT
    Server: WSGIServer/0.2 CPython/3.4.2
    Content-Type: application/json
    Content-Length: 0

    $ curl -X GET localhost:8080/req/not-found; echo
    {"status_name": "404 Not Found", "message": "Nothing here", "status": 404}

    $ curl -X GET localhost:8080/req/no-auth; echo
    {"status_name": "401 Unauthorized", "message": "Go back. You are alien",
    "status": 401}

    $ kill %1
