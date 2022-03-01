#!/bin/bash

docker run --name archicheck-DB --network archicheck-network -e MONGO_INITDB_ROOT_USERNAME=archicheck-db-user -e MONGO_INITDB_ROOT_PASSWORD=archicheck-db-password -d --rm mongo:5.0
docker attach archicheck-DB
