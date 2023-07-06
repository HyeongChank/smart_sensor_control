from flask import Flask, render_template, jsonify, request
import json
import requests
from simulation import simul_vibration
from flask_cors import CORS
import pandas as pd
app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config.update(
    CELERY_BROKER_URL='amqp://localhost//',
    CELERY_RESULT_BACKEND='rpc://'
)

@app.route('/api/dashboard', methods=['GET', 'POST'])
def inputDataPost():
    if request.method == 'GET':
        production_data = simul_vibration.operate_main()
        return jsonify(production_data)

if __name__ == '__main__':
    # host, port를 설정하고 여기로 요청을 하게 하면 됨
    app.run(host='0.0.0.0', port=5000, debug=True)