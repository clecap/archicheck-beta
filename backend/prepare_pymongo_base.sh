#!/bin/bash
# Builds the image with python and the pymongo library installed, that the final web server image is based on.
set -x

docker build -t pymongo_base_image setup/

