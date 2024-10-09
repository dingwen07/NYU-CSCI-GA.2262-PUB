from query import query

data = {
        "hostname": "fibonacci.com",
        "ip": "127.0.0.1",
        "as_ip": "127.0.0.1",
        "as_port": "53533"
}

response = query(data)
print(response)


