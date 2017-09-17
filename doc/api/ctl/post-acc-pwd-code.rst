.. _ctl-post-acc-rpwd-code:

POST /acc/pwd/code
==================

Invoke reset password code. 

On successfully, an email will be send to account's email to inform about
action. It contains code and expired date.

If code was expired, it can use to reset password.

Use that code to reset password in :ref:`ctl-post-acc-rpwd`.

.. text-msg::

    POST /acc/pwd/code
    Content-Type: application/json

    .. text-msg-div::

    .. jsondump:: clink.model.acc.post_rpwd_code

    .. text-msg-div::

    HTTP/1.1 204 No Content
