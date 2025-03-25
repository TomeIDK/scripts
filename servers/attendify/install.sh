#!/bin/bash
echo "Running docker-compose.yml..."
docker compose up -d

if [ $? -ne 0 ]; then
    echo "Failed to execute docker-compose.yml. Exiting."
    exit 1
fi

echo "docker-compose.yml executed successfully."