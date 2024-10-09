from register import register_hostname
import socket

def send_dns_query(data):
    message = f"TYPE=A\r\nNAME={data['hostname']}"
    server_address = (data['as_ip'], int(data['as_port']))

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(message.encode(), server_address)
        response, _ = sock.recvfrom(4096)
        return response.decode()
    
if __name__ == '__main__':
    # Example usage
    data = {
        "hostname": "fibonacci.com",
        "ip": "127.0.0.1",
        "as_ip": "127.0.0.1",
        "as_port": "53533"
    }

    # register_hostname(data)

    response = send_dns_query(data)
    print(f'Received response:\n{response}')
