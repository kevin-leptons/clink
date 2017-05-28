.. _ctl-post-acc-reg-code:

POST /acc/reg/code
==================

Invoke registration code.

On successfully, an message will be send to user's email to inform about
action. It contains registration code and expired date.

If code was expired, temporary account's information can be remove and
other users can register with that information.

Use that code to active account in :ref:`ctl-post-acc-reg`.

.. text-msg::

    POST /acc/reg/code
    Content-Type: application/json

    .. text-msg-div::

    .. jsondump:: clink.model.acc.post_reg_code

    .. text-msg-div::

    HTTP/1.1 204 No Content
