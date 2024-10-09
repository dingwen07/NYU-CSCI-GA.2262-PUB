import socket

def register_hostname(data):

    message = f"TYPE=A\r\nNAME={data['hostname']}\r\nVALUE={data['ip']}\r\nTTL=10\r\n"
    server_address = (data['as_ip'], int(data['as_port']))

    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # Send the message to the AS server
        sock.sendto(message.encode(), server_address)
        print(f"Sent:\n{message}")
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
