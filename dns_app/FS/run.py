from flask import Flask, request
from register import register_hostname
from fibonacci import fibonacci
import re

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello world!'

@app.route('/register', methods=['PUT'])
def register():
    data = request.get_json()
    print(data)
    try:
        register_hostname(data)
        return 'Hostname registered successfully', 201
    except ValueError as e:
        return str(e), 400
    except Exception as e:
        return str(e), 500

@app.route('/fibonacci')
def get_fibonacci():
    number = request.args.get('number')
    if number is None:
        return 'Number parameter is required', 400
    try:
        n = int(number)
        result = fibonacci(n)
        return str(result), 200
    except ValueError:
        return 'Invalid number format', 400

app.run(host='0.0.0.0',
        port=9090,
        debug=True)
