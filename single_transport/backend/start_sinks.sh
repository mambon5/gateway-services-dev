#!/bin/bash

# this files is the responsible one for running the right docker-compose file and start the 3 services.
# there are 2 files here, both contain exactly the same code, and the only difference between them is 
# that they use different USB ports for starting the sink service. This is because 

# Define the path to the Docker Compose file
DOCKER_COMPOSE_FILE_1=docker-compose.yml
DOCKER_COMPOSE_FILE_2=docker-compose_ACM1.yml

# stop services
# docker-compose down

# Execute the Docker Compose file
# this is to delete all previously created and unused networks: (to avoid conflicts)
echo admin | sudo -S docker-compose down

# echo admin | sudo -S docker network prune
# # same for the unused docker containers:
# echo admin | sudo -S docker container prune

echo admin | sudo -S docker-compose -f ../$DOCKER_COMPOSE_FILE_1 up &

# Check for errors in the response
if [ $? -eq 0 ]; then
    echo "Docker Compose file $DOCKER_COMPOSE_FILE_1 executed successfully. Sink running on port ACM0"
else
    echo "Error executing Docker Compose file $DOCKER_COMPOSE_FILE_1, trying tu run sink on ACM1..."
    echo admin | sudo -S docker-compose -f ../$DOCKER_COMPOSE_FILE_2 up &
fi

# printf "11\n5" | python3 otap_menu.py # runs the script that activates (11) all sinks on network address 5.