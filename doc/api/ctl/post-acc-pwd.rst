.. _ctl-post-acc-rpwd:

POST /acc/pwd
=============

Set current password to new password by reset password code.

On successfully, an message will send to account's email to inform about
action. It contains reset password code and expired date.

Get reset password code from :ref:`ctl-post-acc-rpwd-code`.

.. text-msg::

    POST /acc/pwd
    Content-Type: application/json

    .. text-msg-div::

    .. jsondump:: clink.model.acc.post_rpwd

    .. text-msg-div::

    HTTP/1.1 204 No Content
