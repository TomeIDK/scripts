#!/bin/bash

# parameters
# [testing|prod]: determines which environment the rabbitmq server should be deployed in
# => will build paths differently based on which environment is provided

# usage
# 1. sets up correct parameters to deploy to the given environment
# 2. creates a symbolic link between REPO_DIR/ENV/docker-compose.yml and TARGET_DIR/{subdir}/docker-compose.yml
# 3. docker compose up -d in TARGET_DIR

REPO_DIR=$(pwd)
TARGET_DIR="/home/ehbstudent/attendify"
ENV=$1

if [[ -z "$ENV" ]]; then
    echo "Usage: ./deploy.sh [testing|prod]"
    exit 1
fi

# create or overwrite the old symbolic link for an environment
deploy() {
    local subdir="$1"
    local source_path="$REPO_DIR/$ENV/docker-compose.yml"
    local target_path=""

    if [[ -n "$subdir" ]]; then
        target_path="$TARGET_DIR/$subdir/docker-compose.yml"
    else
        target_path="$TARGET_DIR/docker-compose.yml"
    fi

    echo "Deploying $ENV configuration to $target_path"
    ln -sf "$source_path" "$target_path"

    # log if symbolic link was created or overwritten succesfully
    if [ $? -eq 0 ]; then
        echo "Deployed $ENV configuration to $target_path"
    else
        echo -e "Failed to create symbolic link:\nSource: $source_path\nTarget: $target_path"
        exit 1
    fi

    # restart services
    cd "$(dirname "$target_path")"
    docker compose up -d

    echo "$ENV environment deployed and services restarted."
}

case "$ENV" in
    testing)
        deploy "test-environment"
        ;;
    prod)
        deploy
        ;;
    *)
        echo "Invalid environment: $ENV. Use [testing|prod]."
        exit 1
        ;;
esac