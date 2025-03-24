#!/bin/bash

# this script assumes you only want to run 1 mysql server instance simultaneously

CONTAINER_NAME="mysql_server"
INIT_SCRIPT_SRC="./init.sql"
INIT_SCRIPT_DEST="/home/ehbstudent/volumes/mysql/init-scripts"

echo "Creating container with name: mysql_server"

if [ ! -d "$INIT_SCRIPT_DEST" ]; then
    echo "Creating init-scripts directory: $INIT_SCRIPT_DEST"
    mkdir -p "$INIT_SCRIPT_DEST"
fi

if [ ! -f "$INIT_SCRIPT_SRC" ]; then
    echo "Error: $INIT_SCRIPT_SRC does not exist. Exiting."
    exit 1
fi



cp "$INIT_SCRIPT_SRC" "$INIT_SCRIPT_DEST"

if [ $? -ne 0 ]; then
    echo "Error: Failed to copy init.sql to $INIT_SCRIPT_DEST. Exiting."
    exit 1;
fi

echo "Copied init.sql successfully."

docker compose up -d

if [ $? -ne 0 ]; then
    echo "Failed to create the Docker container. Exiting."
    exit 1
fi

echo "Container $CONTAINER_NAME created successfully."
echo "MySQL server created successfully."