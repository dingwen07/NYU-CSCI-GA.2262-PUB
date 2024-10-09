import requests
import random

def print_response(response):
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")

def get_fibonacci_number(x):
    url = f"http://localhost:9090/fibonacci?number={x}"
    response = requests.get(url)
    return response

url = "http://localhost:9090/register"
data = {
    "hostname": "fibonacci.com",
    "ip": "127.0.0.1",
    "as_ip": "127.0.0.1",
    "as_port": "535333"
}

response = requests.put(url, json=data)
print_response(response)

number = random.randint(1, 100)
response = get_fibonacci_number(number)
print_response(response)
print(f"Fibonacci number for {number}: {response.text}")

response = get_fibonacci_number("invalid")
print_response(response)

