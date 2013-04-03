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
    - on exception

Also with customizable templates per each plugin.


instalation to virtualenv
=========================

.. sourcecode:: bash

    git clone git@github.com:matejc/opensezame.git

    # copy over example project
    cp -r opensezame/src/opensezame/example .
    mv example/ myproject/

    # install virtualenv and opensezame into project folder
    virtualenv --no-site-packages myproject/
    cd myproject/
    bin/pip install ../opensezame/


upgrade in virtualenv
=====================

.. sourcecode:: bash

    # cd to local repository
    cd /path/to/opensezame

    git pull

    # cd to project
    cd /path/to/myproject

    # do actual upgrade
    /path/to/myproject/bin/pip install --upgrade /path/to/opensezame/


configuration
=============

.. sourcecode:: bash

    # change directory to where the opensezame.json and bin folder is
    cd /path/to/myproject/

    # edit default configuration if needed
    vim opensezame.json

    # create server key and cert
    openssl req -new -newkey rsa:4096 -days 3650 -nodes -x509 -keyout server.key -out server.crt


writing plugins
===============

    example plugins are in plugins/ folder
    example templates are in templates/ folder

    to create new plugin::

        cp plugins/dostuff.py plugins/myplugin.py
        cp -r templates/dostuff templates/myplugin

        and activate plugin by editing entry *plugins* in *opensezame.json*::

            "plugins": ["dostuff", "mplayer", "myplugin"]


usage
=====

.. sourcecode:: bash

    # change directory to where the opensezame.json and bin folder is
    cd /path/to/myproject/

    # run the server
    bin/opensezame-run

    # in browser:
    https://localhost:9876/myplugin


api
===

Here is **curl** command example for triggering server actions.

.. sourcecode:: bash

    curl --silent -o /dev/null --insecure -w "%{http_code}" \
        --data "passfield=changeme" https://localhost:9876/myplugin


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
    openssl req -new -newkey rsa:4096 -days 3650 -nodes -x509 -keyout server.key -out server.crt

    # run the server
    opensezame-run

    # in browser:
    https://localhost:9876/dostuff
