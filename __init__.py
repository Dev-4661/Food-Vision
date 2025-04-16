from flask import Flask
import os

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = os.urandom(24)  # Generate a secret key

from app import routes 