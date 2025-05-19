#!/bin/bash

# parameters
# mysql_container_id: mysql db docker container id
# create_script_name.sql: name of a sql script prefixed by 'create_'

# usage
# 1. asks for the mysql root password securely
# 2. copies given script and equivalent drop script from SCRIPTS_DIR to VOLUME_DIR
# 3. docker exec -it into given mysql docker container for database 'fossbilling'
# 4. executes the drop script
# 5. executes the create script

# usage check
if [ -z "$2" ]; then
  echo "Usage: $0 <mysql_container_id> <create_script_name.sql>"
  exit 1
fi

read -s -p "Enter MySQL root password: " MYSQL_ROOT_PASSWORD
echo ""

# define paths
SCRIPTS_DIR="./scripts"
VOLUME_DIR="./volumes/mysql/scripts"
REQUIRED_FILES=("${2/create/drop}" $2)
echo "${2/create/drop}"
CONTAINER_NAME="$1"

# verify files exist
for file in "${REQUIRED_FILES[@]}"; do
  if [ ! -f "$SCRIPTS_DIR/$file" ]; then
    echo "Error: File $SCRIPTS_DIR/$file does not exist."
    exit 1
  fi
done

# copy only the required scripts
echo "Copying SQL scripts to $VOLUME_DIR..."
for file in "${REQUIRED_FILES[@]}"; do
  sudo cp "$SCRIPTS_DIR/$file" "$VOLUME_DIR/"
done

# execute into the mysql container and run the scripts
for file in "${REQUIRED_FILES[@]}"; do
  echo "Executing $file inside container..."
  if ! sudo docker exec -i "$CONTAINER_NAME" sh -c \
    "mysql -u root -p\"$MYSQL_ROOT_PASSWORD\" fossbilling < /var/lib/mysql/scripts/$file"; then
    echo "Error executing $file. Exiting."
    exit 1
  fi
done

echo "SQL scripts executed successfully."