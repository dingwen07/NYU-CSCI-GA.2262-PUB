from flask import Flask, request
from query import query
import requests

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello world!'

@app.route('/fibonacci', methods=['GET'])
def fibonacci():
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')

    if not all([hostname, fs_port, number, as_ip, as_port]):
        return "Missing parameters", 400

    data = {
        "hostname": hostname,
        "fs_port": fs_port,
        "number": number,
        "as_ip": as_ip,
        "as_port": as_port
    }

    response = query(data)
    print(response)

    if 'VALUE' not in response:
        return "Error", 500
    if response['VALUE'] == 'NOT_FOUND':
        return "Not found", 404
    
    # send request to fibonacci server
    url = f'http://{response["VALUE"]}:{fs_port}/fibonacci?number={number}'
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        return "Fibonacci server error", 500
    return response.text, response.status_code

app.run(host='0.0.0.0',
        port=8080,
        debug=True)
