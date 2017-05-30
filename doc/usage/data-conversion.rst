Data Conversion
===============

Data conversion divides into two type:

- Request conversion: Depend on request content-type, map raw data into
  Python object. For example, map JSON string into Python dictionary.
  In default, Clink convert JSON string and URL Encode to dictionary or
  list, etc. This handlers must extend from **Lv3Handler** - Pre-Main Handling.

- Response conversion: Depend on response content-type, convert Python
  object into string, because send handler accept string as body of response
  message. In default, Clink convert dictionary, list, etc to JSON string.
  This handlers must extend from **Lv5Handler** - Responding Handling

Now, let create data conversion handlers to know "How it work?". We create
two handlers:

- **ReqTextHandler** converts 'text/plain' to list of words.
- **ResTextHandler** joins list of words to string

And we create main handler to converts list of words to uppercase:
**TextCtl.process_text**

Example
-------

.. literalinclude:: ../example/usage/data_conversion.py
    :language: python
    :caption: data_conversion.py

Testing
-------

.. code-block:: shell-session

    $ python data_conversion.py &> /dev/null &
    [1] 6456

    $ curl -X POST -H "Content-Type: text/plain" \
      -d "my name is kevin" localhost:8080/text; echo
    MY NAME IS KEVIN

    $ kill %1
