#!/bin/bash

now=$(date)
user=$(who | awk '{print $1; exit}')
path="/home/$user/smartec/gateway-services/single_transport/backend"
log_path="$path/logs"

echo "" >> $log_path/logs_mosquitto_server.out
echo "" >> $log_path/logs_sink_service.out
echo "" >> $log_path/logs_gateway_backend.out
echo "" >> $log_path/gateway_services_logs_1.log
echo "" >> $log_path/gateway_services_logs_2.log

echo $now >> $log_path/logs_mosquitto_server.out
echo $now >> $log_path/logs_sink_service.out
echo $now >> $log_path/logs_gateway_backend.out
echo $now >> $log_path/gateway_services_logs_1.log
echo $now >> $log_path/gateway_services_logs_2.log

echo "" >> $log_path/logs_mosquitto_server.out
echo "" >> $log_path/logs_sink_service.out
echo "" >> $log_path/logs_gateway_backend.out
echo "" >> $log_path/gateway_services_logs_1.log
echo "" >> $log_path/gateway_services_logs_2.log

# killall python3 # delete all python scripts running right now
# killall sleep
# killall mosquitto

cd $path

echo admin | sudo -S killall python3 # this line is supposed to kill any remaining python processes that might mess up my code
# echo admin | sudo -S killall mosquitto # this line is supposed to kill the mosquitto broker in order to restart it and keep the detailed logs


./start_mosquitto_server.sh >> $log_path/logs_mosquitto_server.out 2>&1  &
./start_sinks.sh >> $log_path/logs_sink_service.out 2>&1 &
sleep 20
./start_gw_comms.sh >> $log_path/logs_gateway_backend.out &
# ./start_listen_to_cloud.sh >> $log_path/logs_gateway_listen_cloud.out &

./trim_log_output.sh  # trim log files