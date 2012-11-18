==========
OpenSezame
==========

UNDER CONSTRUCTION


This is small HTTP server with SSL support,
with specific purpose, like, activating stuff through web.
Actions can be easily added to events:

    - on index page loaded,
    - on successful entry,
    - on access denied,
    - and more ...

Also with customizable templates.


instalation to virtualenv
=========================

.. sourcecode:: bash

    git clone git@github.com:matejc/opensezame.git
    cp -r opensezame/src/opensezame/example .
    mv example/ myproject/
    virtualenv --no-site-packages myproject/
    cd myproject/
    bin/pip install ../opensezame/


configuration
=============

.. sourcecode:: bash

    # change directory to where the opensezame.json and bin folder is
    cd /path/to/myproject/

    # copy default configuration
    cp opensezame.json.example opensezame.json

    # change your password
    vim opensezame.json

    # create server key and cert
    openssl genrsa -des3 -out server.key 4096
    openssl rsa -in server.key -out server.key.insecure
    mv server.key server.key.secure
    mv server.key.insecure server.key
    openssl req -new -key server.key -out server.csr
    openssl x509 -req -days 3650 -in server.csr -signkey server.key -out server.crt


usage
=====

.. sourcecode:: bash

    # change directory to where the opensezame.json and bin folder is
    cd /path/to/myproject/

    # run the server
    bin/opensezame-run

    # in browser:
    https://localhost:9876/opensezame


api
===

Here is **curl** command example for triggering server actions.

.. sourcecode:: bash

    curl --silent -o /dev/null --insecure -w "%{http_code}" \
        --data "passfield=changeme" https://localhost:9876/opensezame


It returns string 200 on success,
401 on access denied
and 500 on server error.


for developers
==============

.. sourcecode:: bash

    git clone git@github.com:matejc/opensezame.git
    virtualenv --no-site-packages opensezame
    cd opensezame
    source bin/activate
    python bootstrap.py
    buildout

    cd src/opensezame/example/

    # copy default configuration
    cp opensezame.json.example opensezame.json

    # change your password
    vim opensezame.json

    # create server key and cert
    openssl genrsa -des3 -out server.key 4096
    openssl rsa -in server.key -out server.key.insecure
    mv server.key server.key.secure
    mv server.key.insecure server.key
    openssl req -new -key server.key -out server.csr
    openssl x509 -req -days 3650 -in server.csr -signkey server.key -out server.crt

    # run the server
    opensezame-run

    # in browser:
    https://localhost:9876/opensezame
