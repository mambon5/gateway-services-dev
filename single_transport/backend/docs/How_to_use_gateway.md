Basic manual on how to use the gateway through the terminal.

- [Introduction and scripts:](#introduction-and-scripts)
- [Interacting with the gateway](#interacting-with-the-gateway)
- [Interacting with the nodes](#interacting-with-the-nodes)
- [What to do if the gateway or nodes don't respond.](#what-to-do-if-the-gateway-or-nodes-dont-respond)
  - [The Interaction with the gateway doesn't work](#the-interaction-with-the-gateway-doesnt-work)
    - [Restart the gateway linux systemd services](#restart-the-gateway-linux-systemd-services)
  - [The Interaction with the nodes doesn't work](#the-interaction-with-the-nodes-doesnt-work)


# Introduction and scripts:

The python3 file

- `backend_script_cloud_comms.py` for user interaction with the gateway or nodes directly.

allow the user to interact with the gateway and the nodes through the terminal. What is basically happening here, is that the user is acting as if she was the cloud. Every command the user gives using the terminal, will be sent to the global MQTT broker as if the user was the cloud issuing messages to the gateway and nodes.

In order to get started, navigate to the folder that contains these files, usually:

```
smartec/gateway-services/single_transport/backend
```

# Interacting with the gateway

Once you are in the *backend* folder, if you wish to interact with the gateway, run the following commands:

1. `python3 backend_script_cloud_comms.py` to interact with gateway directly.

2. Then enter a 
```5```

This sets the mode to interact with the gateway only.

Now you should set the gateway id, the barcelona big metallic one has id: ``` 618671184831 ```, the one Pablo brought to Oman has id: ``` 114477776340091 ```.

3, Finally enter one of the commands of *Cloud to gateway interaction* listed in the documentation file `Communication_protocols_cloud_to_gateway.md`. For instance, you could now enter a `9` to extract the gateway version. 

# Interacting with the nodes

Once you are in the *backend* folder, if you wish to interact with the nodes, run the following commands:

1. Run the following command `backend_script_cloud_comms.py` for user interaction.

2. Then enter a 
```4```

This sets the mode to interact with the nodes only.

Now you should set the node id, the barcelona nodes so far have ids: ``` 3, 277, 40002 ```, the ones Pablo brought to Oman have ids: ``` 110, 41129 ```.

3. Finally enter one of the commands of *Cloud to node interaction* listed in the documentation file `Communication_protocols_cloud_to_gateway.md`. For instance, you could now enter a `1` to turn on a lamp, or a `14` to extract the node version. 

# What to do if the gateway or nodes don't respond.



If any of the commands listed on the chapters  [Interacting with the nodes](#interacting-with-the-nodes) or [Interacting with the gateway](#interacting-with-the-gateway) fail, then refer to this section.

If both of the connections fail, then first make sure the gateway interactions work, since it is the first layer of communications originating from the cloud, and then try to make the cloud-node communications work.

## The Interaction with the gateway doesn't work

First make sure the gateway is connected to the power, and it has internet via an ethernet cable.

If it still doesn't work, it can be for many reasons:

- The gateway doesn't have internet, make sure the ethernet cable works and gives internet to the gateway
- The gateway is turned off, turn it on if that is the case 

If the gateway still doesn't work, then try one of the following possible error resolutions:

### Restart the gateway linux systemd services

Run the following command on the gateway terminal:

```
sudo systemctl restart gateway_update_code.service
```
This is equivalent to rebooting the gateway itself.

This will download the latest production/dev code and restart the gateway services.

After 2 minutes you can check the last lines in the log file:

```
.../backend/logs/logs_gateway_backend.out
```

If the last line is just a line break, then a date, then another line break, this means the gateway is not working and it didn't start properly. To troubleshoot the error in the python code that made this happen, read the last lines of the log file:

```
.../backend/logs/gateway_services_logs_2.log
```
In this file or the errors in the python code are reported. The logs of each gateway restart are appended to the previous ones, so in order to find the errors since the last time you restarted the gateway, you should start reading on the date and time of the last gateway restart. If the logs for that day and time are just

```
[sudo] contraseña para salvi-smartec: python3: ningún proceso encontrado
```
or they are empty, it means everything is okay with the python code of the gateway.



## The Interaction with the nodes doesn't work

It can be for the following reasons, at least:

- the gateway doesn't respond
- the sink doesn't work or it is not in the right USB port, 
- the sink antenna is not powerful enough to reach the nodes
- the nodes are too far away from the sink
- the nodes firmware program has been rewritten by an active OTAP on the gateway's sink > set the sink to NO OTAP (this can't be done via this cloud interface, only by calling directly the python script `otap_menu.py` and then option 5, on the gateway's program itself.)
- The nodes have a bug in their firmware

Possible mitigation: Try the same as for solving the gateway problems, restart the gateway and check the log files mentioned before.