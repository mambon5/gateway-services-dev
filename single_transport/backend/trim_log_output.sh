
while true; do
    # trim the log files to a finite amount of lines per log file:

    tail -n 4000 logs/logs_mosquitto_server.out > logs/logs_mosquitto_server.out.tmp
    cat logs/logs_mosquitto_server.out.tmp > logs/logs_mosquitto_server.out
    
    tail -n 1000 logs/logs_sink_service.out > logs/logs_sink_service.out.tmp
    cat logs/logs_sink_service.out.tmp > logs/logs_sink_service.out
    
    tail -n 4000 logs/logs_gateway_backend.out > logs/logs_gateway_backend.out.tmp
    cat logs/logs_gateway_backend.out.tmp > logs/logs_gateway_backend.out

    # tail -n 4000 logs/logs_gateway_listen_cloud.out > logs/logs_gateway_listen_cloud.out.tmp
    # cat logs/logs_gateway_listen_cloud.out.tmp > logs/logs_gateway_listen_cloud.out

    # service logs:
    tail -n 10000 logs/gateway_services_logs_1.log > logs/gateway_services_logs_1.tmp
    cat logs/gateway_services_logs_1.tmp > logs/gateway_services_logs_1.log
    tail -n 10000 logs/gateway_services_logs_2.log > logs/gateway_services_logs_2.tmp
    cat logs/gateway_services_logs_2.tmp > logs/gateway_services_logs_2.log

    # delete the temporal log files:

    echo "" > logs/logs_mosquitto_server.out.tmp
    echo "" > logs/logs_sink_service.out.tmp
    echo "" > logs/logs_gateway_backend.out.tmp
    echo "" > logs/gateway_services_logs_1.tmp
    echo "" > logs/gateway_services_logs_2.tmp
    # echo "" > logs/logs_gateway_listen_cloud.out.tmp
    

    sleep 10
done






