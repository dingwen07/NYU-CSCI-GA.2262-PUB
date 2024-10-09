#!/bin/bash

docker run --name dns-app.us -p 8080:8080 -it --rm extrawdw/dns-app.us:latest
