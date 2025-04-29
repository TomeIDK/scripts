#!/bin/bash

# this script assumes you only want to run 1 fossbilling server instance simultaneously

if [ -z "$2" ]; then
    echo "Usage: $(realpath "$0") <host_port> <container_port>"
    exit 1
fi

max_attempts=15
attempt=1
host_port=$1
container_port=$2

echo "Creating docker container..."

while [ $attempt -le $max_attempts ]; do
    id=$RANDOM
    container_name="fb_standalone_$id"

    if ! docker ps -a --format '{{.Names}}' | grep -q "^${container_name}$"; then
        break
    fi

    attempt=$((attempt + 1))
    sleep 1
done

if [ $attempt -gt $max_attempts ]; then
    echo "Failed to generate unique container name after $max_attempts attempts. Exiting."
    exit 1
fi

echo "Creating container with name: $container_name"

docker run -d --name "$container_name" -p $host_port:$container_port -v=fossbilling:/var/www/html --restart=always fossbilling/fossbilling:latest

if [ $? -ne 0 ]; then
    echo "Failed to create the Docker container. Exiting."
    exit 1
fi

echo "Container $container_name created successfully"


echo "Removing old cron jobs..."
# remove old cron jobs
crontab -l | grep -v "docker exec fb_standalone_" | crontab -

echo "Adding new cron job..."
# add cron job
(crontab -l; echo "*/5 * * * * docker exec $container_name su www-data -s /usr/local/bin/php /var/www/html/cron.php")|awk '!x[$0]++'|crontab -

echo "FOSSBilling server created successfully"