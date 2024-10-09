import socket
import re

def register_hostname(data):
    # Validate input data
    required_keys = ['hostname', 'ip', 'as_ip', 'as_port']
    for key in required_keys:
        if key not in data:
            raise ValueError(f"Missing required field: {key}")
        
    # Validate hostname
    if not re.match(r"^[a-zA-Z0-9.-]*$", data['hostname']):
        raise ValueError("Invalid hostname format")

    # Validate IP addresses
    try:
        socket.inet_aton(data['ip'])
        socket.inet_aton(data['as_ip'])
    except socket.error as e:
        raise ValueError(f"Invalid IP address format: {e}")

    # Validate port number
    try:
        port = int(data['as_port'])
        if not (0 <= port <= 65535):
            raise ValueError("Port number must be between 0 and 65535")
    except ValueError as e:
        raise ValueError(f"Invalid port number: {e}")

    message = f"TYPE=A\r\nNAME={data['hostname']}\r\nVALUE={data['ip']}\r\nTTL=10"
    server_address = (data['as_ip'], int(data['as_port']))

    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # Send the message to the AS server
        sock.sendto(message.encode(), server_address)
        print(f"Sent: {message}")
    except Exception as e:
        raise e
    finally:
        sock.close()

if __name__ == '__main__':
    # Example usage
    data = {
        "hostname": "fibonacci.com",
        "ip": "127.0.0.1",
        "as_ip": "127.0.0.1",
        "as_port": "53533"
    }

    register_hostname(data)
