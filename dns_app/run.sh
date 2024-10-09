#!/bin/bash

docker run --name dns-app.fs -p 9090:9090 --rm -d extrawdw/dns-app.fs:latest
docker run --name dns-app.as -p 53533:53533/udp --rm -d extrawdw/dns-app.as:latest
docker run --name dns-app.us -p 8080:8080 --rm -d extrawdw/dns-app.us:latest
