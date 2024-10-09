#!/bin/bash

docker run --name dns-app.fs -p 9090:9090 -it --rm extrawdw/dns-app.fs:latest
