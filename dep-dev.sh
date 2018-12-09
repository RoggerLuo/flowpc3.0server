#! /bin/bash
export FLASK_APP=hello.py
export FLASK_ENV=development
python3 -m flask run --host=0.0.0.0 --port=5555