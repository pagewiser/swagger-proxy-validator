configure:
    virtualenv venv
    source venv/bin/activate
    venv/bin/pip install -r requirements.txt

run:
    source venv/bin/activate
    venv/bin/python proxy.py
