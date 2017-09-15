Development
===========

Installation
------------

Clink is not depends on mongodb server but it's testing do.
Mongodb server is not in standard package repository of Linux distros, 
install it by hand here 
https://docs.mongodb.com/manual/administration/install-on-linux/.

Then follow instructions:

.. code-block:: shell-session

    # essential tools
    $ apt-get install python3 git

    # clone source code
    $ git clone https://github.com/kevin-leptons/clink
    $ cd clink

    # enter virtual environment
    $ ./env init
    $ . venv/bin/active

    # install dependency packages
    $ ./env install

    # create test configuration
    export CLINK_TEST_ROOT_EMAIL='test-mail@gmail.com'
    export CLINK_TEST_ROOT_EMAIL_PWD='test-mail-pwd'
    export CLINK_TEST_ROOT_EMAIL_SERVER='smtp.gmail.com'
    export CLINK_TEST_ROOT_EMAIL_SERVER_PORT='587'

Develop
-------

.. code-block:: shell-session

    # build document
    $ ./ctl doc

    # view document
    $ ./ctl doc --view

    # test
    $ ./ctl test

    # build and push pip package to pypi
    # it required authentication
    $ ./ctl release
