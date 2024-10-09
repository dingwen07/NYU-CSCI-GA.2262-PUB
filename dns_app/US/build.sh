#!/bin/bash

docker build . --platform linux/amd64,linux/arm64 -t extrawdw/dns-app.us:latest
