Swagger proxy validator
=======================

Development
-----------

If you want to develop and maintain this package, you will have to install all the dependencies,
etc. To do so, run:

    python setup.py develop

You can run this command in virtualenv so you will not have the dependencies in the main Python
libraries.

Setup
-----

The proxy is written in Python, you will need Python 2.7 to run the script.

All dependencies are in requirements.txt file, to install it, run:

    pip install -r requirements.txt

If you don't want to install it into your python, use
[virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/).

### On Windows

There is a possibility, that you will need VC compiler for Python, if you see this message
`error: Microsoft Visual C++ 9.0 is required. Get it from http://aka.ms/vcpython27` in the
process of installing dependencies, install VC For Python2.7.

    Link1: http://aka.ms/vcpython27 (slow connection)
    Link2: https://www.microsoft.com/en-ca/download/details.aspx?id=44266

Then you can install everything to virtualenv with these commands:

    pip install virtualenv
    virtualenv venv
    venv/Scripts/activate
    venv/Scripts/pip.exe install -r requirements.txt
    venv/Scripts/pip.exe install -r requirements-win.txt
    or with proxy
    venv/Scripts/pip.exe --proxy="http://........" install -r requirements.txt

### On Linux

_Not tested yet_

Linux comes with prepared make file. For the installation process, run

    make configure

after that, change the configuration script. To start the proxy server, run

    make run

Configuration
-------------

When you first run the script, it will create a configuration file, you can edit it.
The properties are straight forward.

Run
---

Run the script by:

    python SwaggerProxy/proxy.py

Using with swagger
------------------

Change the path to your project in postmane to localhost:8000 or any other port you choose
in the config file.
