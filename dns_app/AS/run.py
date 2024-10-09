import socket
import sqlite3
import threading
import os

DB_FILE = 'dns_records.db'
PORT = 53533

def init_db():
    """Initializes the database and creates the DNS records table if it doesn't exist."""
    if not os.path.exists(DB_FILE):
        open(DB_FILE, 'w').close()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dns_records (
            type TEXT,
            name TEXT,
            value TEXT,
            ttl INTEGER,
            PRIMARY KEY (type, name)
        )
    ''')
    conn.commit()
    conn.close()

def handle_registration(data):
    """Handles the registration of DNS records."""
    lines = data.splitlines()
    record = {}
    for line in lines:
        key, value = line.split('=')
        record[key.lower()] = value

    if 'type' not in record or 'name' not in record or 'value' not in record or 'ttl' not in record:
        return "ERROR: Missing required fields for registration"

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO dns_records (type, name, value, ttl)
        VALUES (?, ?, ?, ?)
    ''', (record['type'], record['name'], record['value'], int(record['ttl'])))
    conn.commit()
    conn.close()

    return f"Registration successful for {record['type']} record\n"

def handle_query(data):
    """Handles the query of DNS records."""
    lines = data.splitlines()
    query = {}
    for line in lines:
        key, value = line.split('=')
        query[key.lower()] = value

    if 'type' not in query or 'name' not in query:
        return "ERROR: Missing required fields for query"

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT value, ttl FROM dns_records WHERE type=? AND name=?', (query['type'], query['name']))
    result = cursor.fetchone()
    conn.close()

    if result:
        value, ttl = result
        response = f"TYPE={query['type']}\r\nNAME={query['name']}\r\nVALUE={value}\r\nTTL={ttl}\r\n"
    else:
        response = f"TYPE={query['type']}\r\nNAME={query['name']}\r\nVALUE=NOT_FOUND\r\nTTL=0\r\n"
    
    return response

def handle_client(data, addr, server_socket):
    """Handles incoming client data."""
    try:
        if data.startswith("TYPE="):
            if "VALUE=" in data and "TTL=" in data:
                response = handle_registration(data)
            else:
                response = handle_query(data)
        else:
            response = "ERROR: Invalid request format\n"
        
        server_socket.sendto(response.encode('utf-8'), addr)
    except Exception as e:
        server_socket.sendto(f"ERROR: {str(e)}\n".encode('utf-8'), addr)

def start_server():
    """Starts the DNS-like server using UDP."""
    init_db()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('0.0.0.0', PORT))
    print(f"DNS server is running on port {PORT} (UDP)")

    while True:
        data, addr = server_socket.recvfrom(4096)
        print(f"Received data from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(data.decode('utf-8'), addr, server_socket))
        client_handler.start()

if __name__ == "__main__":
    start_server()
