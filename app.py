from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app
from flask import Response, Flask, jsonify
import py_eureka_client.eureka_client as eureka_client
import os

 
app = Flask(__name__)
EUREKA_URL = os.getenv("EUREKA_URL", "http://127.0.0.1:8761/eureka")
APP_NAME = os.getenv("APP_NAME", "pyapp-demo")
SERVER_PORT = 8000
eureka_client.init(eureka_server=EUREKA_URL,
                   app_name=APP_NAME,
                   instance_port=SERVER_PORT,
                   ha_strategy=eureka_client.HA_STRATEGY_RANDOM)
app_dispatch = DispatcherMiddleware(app, {'/metrics': make_wsgi_app()})

@app.route('/info')
def info():
    info = {
        'metrics-path': '/metrics',
        'version': '0.1.2'
    }
    return jsonify(info), 200

@app.route('/')
def index():
    return jsonify({
        'Flask': 'flask-1.1.1',
        'Werkzeug': 'Werkzeug-0.16.0',
        'Prometheus-Client': 'prometheus-client-0.7.1',
        'Py-Eureka-Client': 'py-eureka-client-0.7.4'
    }), 200
 
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=SERVER_PORT)
