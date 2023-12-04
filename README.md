# Gateway backend 

## Summary

This is the backend server for the gateway. The code is written in python. The idea of this backend is to act as a *bridge* between the cloud and the nodes, while storing some rellevant information for later use that the cloud might require. In particular it will:

1. Connect to the global MQTT broker hosted by a global server
2. Host a local MQTT broker that will be the entry point of all the node messages via the sink.
3. Transmit any neccessary communicatiosn between the global broker and the nodes.

## Main script

The main gateway python API script for:

1. *cloud communications* is called `backend_script_cloud_comms.py` 
2. *node communications* is called `backend_script_node_comms.py`. 
   
Both are located in `single_transport/backend/` . They are both modifications of the original wirepas app called `script_evaluation_app.py`.

## Documentation

1. The documentation of the **gateway to cloud/node functionality** is all placed at [`Gateway manual`](https://github.com/smartec-lighting/gateway-services-development/tree/main/single_transport/backend/docs/gateway_manual.md)
2. The documentation on the gateway API **python code**, is placed at `gateway-services/single_transport/code-docs/build/html/index.html` also readable here > https://demokrafist.000webhostapp.com/gateway_api_doc/
