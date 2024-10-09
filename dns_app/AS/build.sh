#!/bin/bash

docker build . --platform linux/amd64,linux/arm64 -t extrawdw/dns-app.as:latest
# delete old container
docker rm -f dns-app.as
