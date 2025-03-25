#!/bin/bash

# this script assumes you only want to run 1 rabbitmq server instance simultaneously

if [ -z "$3" ]; then
    echo "Usage: $(realpath "$0") <user> <password> <management_port> <amqp_port>"
    exit 1
fi

user=$1
password=$2
management_port=$3
amqp_port=$4

echo "Creating container with name: rabbitmq"

# latest RabbitMQ 4.0.x
docker run -d --hostname my-rabbit --name some-rabbit -e RABBITMQ_DEFAULT_USER=$user -e RABBITMQ_DEFAULT_PASS=$password -e RABBITMQ_DEFAULT_VHOST=attendify -v /home/ehbstudent/volumes/rabbitmq:/var/lib/rabbitmq -p $management_port:15672 -p $amqp_port:5672 rabbitmq:4-management


if [ $? -ne 0 ]; then
    echo "Failed to create the Docker container. Exiting."
    exit 1
fi

echo "Container rabbitmq created successfully"


echo "RabbitMQ server created successfully"