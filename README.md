Swagger proxy validator
=======================

Setup
-----

The proxy is written in Python, you will need Python 2.7 to run the script.

All dependencies are in requirements.txt file, to install it, run:

    pip install -r requirements.txt

If you don't want to install it into your python, use [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/).

Configuration
-------------

There is no configuration yet, to change the url of the application, change it in proxy.py file.

Run
---

Run the script by

    python proxy.py

Using with swagger
------------------

Change the path to your project in swagger to localhost:8000.
