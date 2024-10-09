#!/bin/bash

docker run --name dns-app.as -p 53533:53533/udp -it extrawdw/dns-app.as:latest
