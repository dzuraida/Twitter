from flask import Flask, Blueprint, request
from twitter import tweeps_api
# from riki_have_this import tweeps_api
import debugger
import twitter
# import riki_have_this

apps = Flask(__name__)
apps.register_blueprint(tweeps_api, url_prefix = '/api/v1/')
# apps.register_blueprint(tweeps_api, url_prefix = '/api/v1/')

@apps.route('/')
def hello():
    return "Hello"

if __name__ == '__main__':
    apps.run(debug=debugger.DEBUG, host=debugger.HOST, port=debugger.PORT)
