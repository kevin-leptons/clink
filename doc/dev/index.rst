Development
===========

Installation
------------

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
    $ cat > tmp/test_conf.py 
    ROOT_EMAIL = 'test-mail@gmail.com'
    ROOT_EMAIL_PWD = 'test-mail-pwd'
    ROOT_EMAIL_SERVER = 'smtp.gmail.com:587'

    # Press Ctrl + C to terminal 'cat' and save test_conf file

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
