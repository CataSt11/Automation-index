import sys
sys.path.insert(0, "./app")
import functions

from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from app import routes
from app import functions
