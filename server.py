#!/usr/bin/env python3
import dotenv
import os
from app import app

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
dotenv.load_dotenv(dotenv_path)
APP_RUN_HOST = os.environ.get("APP_RUN_HOST", "0.0.0.0")
APP_RUN_PORT = os.environ.get("APP_RUN_PORT", "5000")
APP_DEBUG = os.environ.get("APP_DEBUG", "1")
if APP_DEBUG not in ["0", "1"]:
    raise Exception("Error: environment variable APP_DEBUG is not '0' or '1'.")
APP_DEBUG = bool(int(APP_DEBUG))


if __name__ == '__main__':
    app.run(debug=APP_DEBUG, host=APP_RUN_HOST, port=APP_RUN_PORT)
