from flask import Flask, request, Blueprint, redirect
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import config
import time
import datetime
import schedule
import threading
from api.v1 import api
from core import cache, limiter
from api.users_ns import users_ns
from api.mac_ns import mac_ns
from api.schedule_ns import schedule_ns

app = Flask(__name__)

VERSION = (1,0)
AUTHOR = 'Darío García Malpica'

def get_version():
    """
    This function returns the API version that is being used.
    """

    return '.'.join(map(str, VERSION))


def get_authors():
    """
    This function returns the API's author name.
    """

    return str(AUTHOR)


__version__ = get_version()
__author__ = get_authors()



namespaces = [ users_ns , mac_ns,schedule_ns]
@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

@app.route('/')
def register_redirection():
    """
    Redirects to documentation page
    """
    return redirect(f'{request.url_root}/{config.URL_PREFIX}', code=302)

def schedule_powerOn():
    while True:
        schedule.run_pending()
        print("I'm running on thread %s" % threading.current_thread())
        time.sleep(60)

def initialize_app(flask_app):
    """
    This function initializes the Flask Application, adds the namespace,registers the blueprint configures the JWT and starts the schedule thread.
    """

    CORS(flask_app,supports_credentials=True,resources={r'/*': {'origins': '*'}})

    v1 = Blueprint('api', __name__, url_prefix=config.URL_PREFIX)
    api.init_app(v1)
    limiter.exempt(v1)
    cache.init_app(flask_app)
    app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
    app.config['JWT_TOKEN_LOCATION'] = ['headers', 'query_string']
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(hours=3)
    jwt = JWTManager(app)
    flask_app.register_blueprint(v1)
    flask_app.config.from_object(config)

    for ns in namespaces:
        api.add_namespace(ns)

    job_thread = threading.Thread(target=schedule_powerOn)
    job_thread.start()

def main():
    initialize_app(app)
    separator_str = ''.join(map(str, ["=" for i in range(175)]))
    print(separator_str)
    print(f'Debug mode: {config.DEBUG_MODE}')
    print(f'Authors: {get_authors()}')
    print(f'Version: {get_version()}')
    print(f'Base URL: http://localhost:{config.PORT}{config.URL_PREFIX}')
    print(separator_str)
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG_MODE, use_reloader=False)



if __name__ == '__main__':
    main()
