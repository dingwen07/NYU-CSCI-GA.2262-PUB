import socket

def query(data):
    if 'type' not in data:
        data['type'] = 'A'
    request_format = f'TYPE={data["type"]}\r\nNAME={data["hostname"]}\r\n'
    server_address = (data["as_ip"], int(data["as_port"]))
    
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        # Send the request
        sock.sendto(request_format.encode(), server_address)
        
        # Receive the response
        response, _ = sock.recvfrom(4096)
        response = response.decode()
        
        # Parse the response
        response_parts = response.split()
        response_dict = {}
        for part in response_parts:
            if '=' not in part:
                continue
            key, value = part.split('=')
            response_dict[key] = value
        
        return response_dict
    finally:
        sock.close()
