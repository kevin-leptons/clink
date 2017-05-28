.. _ctl-post-acc-reg:

POST /acc/reg
=============

Active account with registration code.

On successfully, an message will be send to user's email to inform about
action. Then account becomes avaiable on system and user can use that 
account.

Get registration from :ref:`ctl-post-acc-reg-code`.

.. text-msg::

    POST /acc/reg
    Content-Type: application/json

    .. text-msg-div::

    .. jsondump:: clink.model.acc.post_reg

    .. text-msg-div::

    HTTP/1.1 204 No Content
