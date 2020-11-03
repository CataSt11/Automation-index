import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '8777fc34-5499-4662-a91a-1adb9609fb1c'
