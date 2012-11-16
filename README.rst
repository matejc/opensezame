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


development instalation
=======================

.. sourcecode:: bash

    git clone git@github.com:matejc/opensezame.git
    virtualenv-2.7 --no-site-packages opensezame
    cd opensezame
    source bin/activate
    python bootstrap.py
    buildout

    # copy default configuration
    cp src/opensezame/opensezame.json.example src/opensezame/opensezame.json

    # change your password
    vim src/opensezame/opensezame.json

    # create server key and cert
    openssl genrsa -des3 -out server.key 4096
    openssl rsa -in server.key -out server.key.insecure
    mv server.key server.key.secure
    mv server.key.insecure server.key
    openssl req -new -key server.key -out server.csr
    openssl x509 -req -days 3650 -in server.csr -signkey server.key -out server.crt

    # run the server
    python src/opensezame/__init__.py

    # in browser:
    https://localhost:9876/opensezame
