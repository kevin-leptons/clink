Pipe Line
=========

General Model
-------------

.. code-block:: text

                        handler-0                        handler-n
                           |                                |
    [o]---[req, res]---[req, res]---[req, res]---....---[req, res]------>[x]
     |                                   |                                |
    in msg                            handler-i                      out msg

**in msg** is HTTP request message from client. **out msg** is HTTP response
message to client. **handler-i** is handler i-th in pipe line. **req** and
**res** store data during processing.

In starting of HTTP request message, two object are created
**req** and **res**. **req** contains data of incoming message such as
remote address, query string, body of messgae, etc. **res** contains
data of response message such as header, body of message, etc.

Then application calls handlers from 0 to n to process request. Each handler
do something with **[req, res]**. It can reads data from
**req**, writes data to **res**.

Final, application send back **res** to client, finish request processing.

Detail Model
------------

.. code-block:: text

       [o]------- in msg
        |
    [req, res]--- lv 0: receiving handling                              [1]
        |
    [req, res]--- lv 1: pre-routing handling                            [n]
        |
    [req, res]--- lv 2: routing                                         [1]
        |
    [req, res]--- lv 3: pre-main handling                               [n]
        |
    [req, res]--- lv 4: main handling                                   [1]
        |
    [req, res]--- lv 5: responding handling                             [n]
        |
    [req, res]--- lv 6: sending handling                                [1]
        |           |
       [x]          |--- error occurs
     out msg        |
                [req, res]--- lv 7: error handling                      [n]
                    |
                [req, res]--- lv 8: error logging handling              [1]
                    |
                [req, res]--- lv 9: error sending handling              [1]
                    |           |
                   [x]          |--- error occurs
                 out msg        |--- server application handling
                                |
                               [x]
                            undefined

Right number is number of handlers. **n** mean that 0 to n. 1 mean that only
one.

Level 0: Receiving Handling
---------------------------

This level MUST be perform quickly. First action is create **req**,
set request data such as query string, header, body message in
stream format and other default values to it. Second action is
create **req** and set default values to it.

Level 1: Pre-routing Handling
-----------------------------

This level MUST be perform quickly. Normal, this level contains one
handler. it performs request logging.

Level 2: Routing
----------------

This level MUST be perform quickly. It finds main handler to perform in
level 4 from request method, path and content type.

Level 3: Pre-main Handling
--------------------------

This level perform data converting such as convert JSON text to
Python dictionary. Be careful, if this level contains too many handlers,
it causes performance issue.

Level 4: Main Handling
----------------------

This is main processing what developer MUST defines. For example,
client send POST request with data in JSON format to application:

    {"name": "A book", "author": "Some body"}

It mean that application MUST create new book with above data. Other levels
doesn't do it. After all, it only finds main handling, maps
text data into Python dictionary and call main handling with [req, res].
This level MUST validate data, put it to datbase and set response data.
Then next levels will send data to client.

Level 5: Responding Handling
----------------------------

This level perform data converting such as convert dictionary to text format.
Be careful, if this level contains too many handlers, it causes performance
issues.

Level 6: Sending Handling
-------------------------

This level receive input as text stream, or string then send it to client.

Level 7: Error Handling
-----------------------

If from level 0 to level 6 causes error, this level handles for it. It
can changes [req, res] content. Main target of this level is provide
HTTP Status Code and Message to client.

Level 8: Error Logging Handling
-------------------------------

Normal, this level contains one handler, it performs log error information.

Level 9: Error Sending Handling
-------------------------------

Send **res** to client. Note that **res** was handled, set Status Code and
Message correspond with error was occurs.

Exception
---------

After all, if any error occurs during level 7 to level 9, it is handle by
server program.
