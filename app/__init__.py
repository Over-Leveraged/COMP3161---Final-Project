from flask import Flask

app = Flask(__name__)
from app import routes

import sys
sys.path.append('dbcon.py')