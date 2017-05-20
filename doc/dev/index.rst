Development
===========

Installation
------------

.. code-block:: bash

    # essential tools
    apt-get install python3 git

    # clone source code
    git clone https://github.com/kevin-leptons/clink
    cd clink

    # enter virtual environment
    ./env init
    . venv/bin/active

    # install dependency packages
    ./env install

Develop
-------

.. code-block:: bash

    # build document
    ./ctl doc

    # view document
    ./ctl doc --view

    # run unit test
    ./ctl test

    # build and push pip package to pypi
    # it required authentication
    ./ctl release
