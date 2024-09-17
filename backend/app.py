#!usr/bin/env python3
"""Setting up my flask app."""

from flask import Flask
from flask_wtf import CSRFProtect

app = Flask(__name__)
app.config.from_object('config')
crsf = CSRFProtect(app)

from routes import *

# ... Flask-Security configuration and initialization (if applicable)

if __name__ == '__main__':
    app.run(debug=True)
