OAuthSv
=======

.. autoclass:: clink.service.OAuthSv

Notes
-----

It doesn't support all of OAuth2 specification, here are supported features:

- RFC 6749, section 4.3 -  Resource Owner Password Credentials Grant
- RFC 6749, section 6 - Refreshing an Access Token
- RFC 7519 - JSON Web Token

Other specifications isn't supported because it's complicated without
browsers. For example, mobile device need polls auth server to gets token
instead of gets it from auth provider directly.

Use this limited OAuth specification, you can't perform external login
with other OAuth Providers, you can only use name-password to get
token and refresh that token. However, it work in simply on all 
of platform.

It also ignore authorization 'scope'. Authorization is perform by
query database, not by information in access_token.

Example
-------

.. literalinclude:: ../sample/api/oauth_sv.py
    :language: python

.. code-block:: shell-session

    $ python oauth_sv.py

Testing
-------

.. code-block:: shell-session

    $ python oauth_sv.py
    token_type: Bearer...
    refresh_token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUx...
    expires_in: 1495561355.3989384...
    access_token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUx...