#!/bin/bash

# Check if IP_ADDRESS is provided as a command-line argument
if [ -z "$1" ]; then
  echo "Usage: $0 <IP_ADDRESS>"
  exit 1
fi

# Assign the first argument to IP_ADDRESS variable
IP_ADDRESS="$1"

echo "FS Register"
# Define the JSON payload with the IP_ADDRESS variable
json_payload=$(cat <<EOF
{
    "hostname": "fibonacci.com",
    "ip": "$IP_ADDRESS",
    "as_ip": "$IP_ADDRESS",
    "as_port": "53533"
}
EOF
)

# Send the JSON payload using HTTP PUT to http://localhost:9090/register
curl -X PUT -H "Content-Type: application/json" -d "$json_payload" http://localhost:9090/register
echo ""

echo "FS Query"
curl -s "$IP_ADDRESS:9090/fibonacci?number=10"
echo ""

echo "AS Query"
python3 test.py

echo "US Query"
curl -s "http://$IP_ADDRESS:8080/fibonacci?hostname=fibonacci.com&fs_port=9090&number=25&as_ip=$IP_ADDRESS&as_port=53533"
echo ""

echo "Done."
