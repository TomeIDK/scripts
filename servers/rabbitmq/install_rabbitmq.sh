#!/bin/bash

# this script assumes you only want to run 1 rabbitmq server instance simultaneously

if [ -z "$2" ]; then
    echo "Usage: $(realpath "$0") <amqp_port> <management_port>"
    exit 1
fi

amqp_port=$1
management_port=$2

echo "Creating container with name: rabbitmq"

# latest RabbitMQ 4.0.x
docker run -it --rm --name rabbitmq -p $amqp_port:5672 -p $management_port:15672 rabbitmq:4.0-management

if [ $? -ne 0 ]; then
    echo "Failed to create the Docker container. Exiting."
    exit 1
fi

echo "Container rabbitmq created successfully"


echo "RabbitMQ server created successfully"