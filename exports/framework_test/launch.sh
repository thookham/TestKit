#!/bin/bash
# Launch Script for framework-laptop-13-(intel-13th-gen)-windows-11-v1
# Builds and runs the Docker container
echo "Starting framework-laptop-13-(intel-13th-gen)-windows-11-v1 environment..."
docker build -t testkit-framework-laptop-13-(intel-13th-gen)-windows-11-v1 -f framework-laptop-13-(intel-13th-gen)-windows-11-v1.Dockerfile .
docker run -it --rm testkit-framework-laptop-13-(intel-13th-gen)-windows-11-v1
