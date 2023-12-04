# Gateway functionality



1. [Introduction. ](#introduction)
    - [Types of messages](#types-of-messages)

## Introduction

Here we will explain what the gateway does.


## Types of messages

1. It can receive messages from the cloud (which in turn may be sent by the **front-end** user)
2. It can receive autonomous messages from the **cloud** (without the front-end)
3. It can receive autonomous messages from the **node**, which mainly contain information messages regarding the driver or node parameters. 

Then it usually processes the previous messages, and either stores information on the local database concerning the message or/and sends a message to the desired entity.

4. It can send messages to the cloud, sending information.
5. It can send messages to the node, either sending an action or requesting information or sending information.

### Message generation

Messages are created by different scripts depending if they are inteded for the cloud or for the nodes. For each interlocutor, there is a file that keeps track of the last message id that was used, and increments it by 1, when a new messages is created. These files are called `local_settings.py` for node messages and `cloud_settings.py` for cloud messages.


## Processing

Based on the messages received, the gateway may have to process the message and decide what to do next.

### Tunneling to node

Depending on the messages from the *front-end*, the gateway may have to transmit them to the mesh network. This is done via the python class *interaction_tunnel*.

There are two kind of *tunnels*.

1. One for the messages of the flow *front-end -> cloud -> gateway -> specific node*
2. Another one for the *front-end -> cloud -> gateway* messages, that the gateway is supposed to broadcast to all the nodes of a *certain client*

### Listening to the nodes

The gateway automatically listens for any message coming from the nodes. This is done via the `systemd` *linux service* called **gateway_service.service**. As soon as it detects one, it registers that new node in an internal variable called *node_list* and automatically creates a tunnel to the cloud, and starts paying attention for any message from the cloud directed to that node.

Moreover, when the gateway restarts, it does a quick *otap* to the sink, and records any node that the sink can detect in this variable called *node_list*. After this, and as part of the gateway startup process, the gateway opens an MQTT subscription to the global broker for every node in this list. This is additional to what was described in the previous paragraph. So both actions take place, to ensure the fastest way to establish a communication between the node and the cloud.

### Listening to the cloud

The gateway automatically listens or subscribes to the MQTT topic `cl-req/gw/<gateway_id>` where the *cloud* publiches the cloud > gw messages. This script is started from the shell script called `start_listen_cloud.sh`.

1. There is a file called `gateway_id.txt` that just keeps track of the gateway id, so that the separate script (from the node interaction) that is reponsible for listening to the cloud, knows the gateway id, without having to create a new WNI interface that can mess up the mesh network already created.

### Store in local database

The gateway must store in the local database:

1. The following **electrical parameters**, for each node, at every time there has been a change:
    1. **voltage** (volts) 0-300 (2 bytes)
    2. **current** (milli amperes) 200-1500 (2 bytes)
    3. **power** (watts) 0-600 (2 bytes)
    4. **power line frequency** (Hz) 0-180 (1 byte)
    5. **light level %** (0-100) (1 byte)
    6. **running hours** (in minutes, for 8100 years) (4 bytes)
    7. **change type** (1-4) type of change that is being reported. Possible values:
        - *Error* -- the reason of the change in current is unknown
        - *strategy* -- the change in current is due to a new strategy being implemented
        - *front-end* -- there has been a user command to directly change the state of a certain led
        - *sensor* -- the movement sensor detected a movement (or no movememnt for a certain ammount of time, and turned the led on/off

2. The **node status metrics**, for each node, at every time there has been a change:
    . **node id** unique node identifier, can be stored in 8 bytes, so it can be up to 256^8
    - **led status** can either be 0 or 1 for closed or open.
    - **dimming** ranges between 0-100 %
    - **neighbours** ranges between 0-10 million
    - **rssi** ranges betweeen -100 and 0 dBm *(0 is the best possible signal)*
    - **hops** ranges betweeen 0 to 256, *(it is the number of jumps a node does to other nodes before reaching a gateway)* The gateway can get this number just from the wirepas message heather.
    - **travel time** we can measure the distance from the node and gateway using the metric of *travel time* which is attached to every message the node sends to the gateway. This time can lay anywhere from *20 milliseconds* to *10 seconds*

3. A list of the **node ids** together with their **client id** for the current nodes that it can see.

4. Strategy list

