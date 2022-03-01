#!/bin/bash

# Builds the final web server container (which includes copying the current version of python-web-server.py to the image) and runs the resulting container.

set -xe

docker build -t python_server_image .
# Read DB credentials into shell variables:
. db.conf

# Start the container with credentials set as environment variables:
docker run --network archicheck-network -it --rm --name python_web_server -p 8080:80 -e "dbusername=$dbusername" -e "dbpassword=$dbpassword" python_server_image
