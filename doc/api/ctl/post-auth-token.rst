.. _ctl-post-auth-token:

POST /auth/token
================

Invoke token.

Use password
------------

.. text-msg::

    POST /auth/token
    Content-Type: application/json

    .. text-msg-div::

    .. jsondump:: clink.model.auth.post_token_pwd

    .. text-msg-div::

    HTTP/1.1 200 OK
    Content-Type: application/json

    .. text-msg-div::

    .. jsondump:: clink.model.auth.res_bearer_token

Use refresh token
-----------------

.. text-msg::

    POST /auth/token
    Content-Type: application/json

    .. text-msg-div::

    .. jsondump:: clink.model.auth.post_token_rtoken

    .. text-msg-div::

    HTTP/1.1 200 OK
    Content-Type: application/json

    .. text-msg-div::

    .. jsondump:: clink.model.auth.res_bearer_token
