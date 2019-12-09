from flask import Flask
from fwt.models import db
from sys import path

app = Flask(__name__)

db.init_app(app)

import fwt.views
