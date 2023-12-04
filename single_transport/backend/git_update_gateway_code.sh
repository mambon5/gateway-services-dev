#!/bin/bash

# sudo systemctl stop gateway_services.service
# sleep 2
user=$(who | awk '{print $1; exit}')
path="/home/$user/smartec/gateway-services/single_transport/backend"

cd $path
./set_git_credentials.sh
git fetch --all
git reset --hard origin

echo admin | sudo -S chmod -R 777 logs # in order to make all logs available to everyone

# sleep(2)
# sudo systemctl daemon-reload
# the following command runs the "sudo" mode with root privileges, and provides the password "admin" using the -S flag and "echo"
echo admin | sudo -S systemctl restart gateway_services.service



