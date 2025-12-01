#!/bin/bash
# Launch Script for raspberry-pi-4-model-b-windows-11-v109
# Builds and runs the Docker container
echo "Starting raspberry-pi-4-model-b-windows-11-v109 environment..."
docker build -t testkit-raspberry-pi-4-model-b-windows-11-v109 -f raspberry-pi-4-model-b-windows-11-v109.Dockerfile .
docker run -it --rm testkit-raspberry-pi-4-model-b-windows-11-v109
