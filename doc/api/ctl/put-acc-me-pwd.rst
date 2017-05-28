PUT /acc/me/pwd
===============

Change password.

On successfully, an email will be send to account's email to inform about
action.

.. text-msg::

    PUT /acc/pwd
    Authorization: <bearer-token>
    Content-Type: application/json

    .. text-msg-div::

    .. jsondump:: clink.model.acc.put_pwd

    .. text-msg-div::

    HTTP/1.1 204 No Content
