# Communication protocols between Gateway and Nodes



- [Communication protocols between Gateway and Nodes](#communication-protocols-between-gateway-and-nodes)
  - [Introduction](#introduction)
  - [Different kind of messages:](#different-kind-of-messages)
  - [Message content](#message-content)
    - [Explanation of the message fields:](#explanation-of-the-message-fields)
    - [Gateway requests to node](#gateway-requests-to-node)
    - [Node requests to gateway](#node-requests-to-gateway)
  - [Cloud messaging](#cloud-messaging)

## Introduction

In this file we explain the basic theory in the communications between the local backend of a gateway, and the mesh networks aka the nodes. We will:

1. Define the content of each message, and how it has to be sent

## Different kind of messages:

We have the following different kind of messages between the gateway and the nodes:

1. Gateway requests to node(s). In the local MQTT broker this is published to `gw-request/send_data/<gw-id>/<sink-id>`:

    - `send action` : These commands comprise the **On, Off, dimming, blink, strategy** requests.
    - `request information` : These requests comprise the **echo, led_status, dimming_status, neighbours, rssi, node_status** requests
    - The response from the mesh network to these messages is published in the local MQTT broker topic: `gw-event/received_data/<gw-id>/<sink-id>/<net_id>/<src_ep>/<dst_ep>` but that is not important for our developper or user purposes. It is more a curiosity of how wirepas works.

2. Node request to gateway. In the local MQTT broker this is published to `gw-event/received_data/<gw-id>/<sink-id>/<net_id>/<src_ep>/<dst_ep>`:

    - `request information` : These commands comprise the **QueHoraEs** request. 
    - `give information` : Thse commands comprise the **alarm, consum** requests
    - The response from the gateway to these messages is published in the local MQTT broker topic: `gw-request/send_data/<gw-id>/<sink-id>` but that is not important for our developper or user purposes. It is more a curiosity of how wirepas works.


A part from the main request, the receiving end will send back a **response message** as soon as it receives and processes the request, to inform the sender that the message was received and processed as expected. This response message is identical to the request itself if all the communication and task were successful, and it gives an error number if the task to be performed fails. Details on each different request and what the response should contain, will be detailed in the next section.

You can see that from a user that is using the wirepass interface, we basically have just 2 MQTT topics for interacting between the *mesh network* and the *gateway backend*. This makes us choose very different message to make sure that a message either belongs to a Gateway request or to a node request.


## Message content

Here we describe the content of each message sent to each machine. The information includes the values sent, a short description, the number of bytes, and the information contained in each byte of the message.

**Note:** Notice that wirepass transforms the payload we send, and adds extra information such as 
- destination_address
- source_endpoint
- destination_endpoint
- qos
- payload *<-- the initial payload*
- initial_delay_ms *(if initial_delay_ms > 0)*
- is_unack_csma_ca *(if is_unack_csma_ca is True)*
- hop_limit *(if hop_limit > 0)*
For instance, if we just want to send a "send action" command from gateway to node, containing a message id of *1022* and a message type of *3* (3 bytes in total), the wirepass libraries end up sending around 33 bytes of message. Thus it appends around 30 bytes to each sent message in order to use the wirepass technology and ensure its optimal distribution.

### Explanation of the message fields:

- The first term is the *message id* and has 2 bytes (H - unsigned long int)
- The second term is the *message type*. We only use 1 byte for this, therefore we have 256 different message types to use. In the gateway-backend to node communication we reserved the values 1-128 for gateway messages to node, and the numbers 129 to 255 for node messages to gateway. 
- the third to the last term are *message arguments* that depend on the specific message type. Some messages have more arguments, some don't have any.
-  Each value of the message is encoded according to the format of the reference https://docs.python.org/3/library/struct.html. Each value must therefore be encoded in either **1 byte** (B,b), **2 bytes**(H), **4 bytes**(i,I) or **8 bytes**(q,Q) to be platform independent. 

### Gateway requests to node

1. Gateway requests to a (or all) the nodes.
2. Message type: The request is specified in the **call** columns and the response to it in the **response** columns:

|message name   | description   | field type    | Call - values | call - bytes  | response - values | response - bytes  | developed by node | developed by gateway | tested the connection | 
|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|:-----------------:|:-----------------:|:-------------:|:-------------:|:-------------:|
|led on         | turn led on   | send action       |[  msg_id(H) msg_type=**1** (B) ]    |    3          |[  msg_id(H) msg_type=**1** (B) ]        | 3                 | OK | OK | OK |
|led off        | switch led off| send action       |[  msg_id(H) msg_type=**2** (B) ]   |    3          |[  msg_id(H) msg_type=**2** (B) ]       | 3                | OK | OK | OK |
|dimming        | set dimming for led| send action       |[  msg_id(H) msg_type=**3** (B) dimming(b) ]   |    4          |[  msg_id(H) msg_type=**3** (B) dimming(b) ]       | 4                | OK | OK | OK |
|blink        | start blinking| send action       | [ msg_id(H) msg_type=**4** (B) ]   |    3          |[  msg_id(H) msg_type=**4** (B) ]       | 3                | OK | OK | OK |
|strategy        | send a lighting strategy| send action       |[  msg_id(H) msg_type=**5** (B) strategy(B) ]   |    4          |[  msg_id(H) msg_type=**5** (B) strategy(B) ]       | 4                | NO (responds with strategy 21 always) | OK | NO |
|echo        | requests the  node to run an echo command. Gateway iniciative | request information       | [  msg_id(H) msg_type=**6** (B) ]   |    3          |[  msg_id(H) msg_type=**6** (B) traveltime(I) ]       | 7                | OK | OK | OK |
|led status        | requests led status | request information       |[  msg_id(H) msg_type=**7** (B) ]   |    3          |[  msg_id(H) msg_type=**7** (B) let_status(B) ]       | 4        | OK | OK | NO (node invents value) |
|dimming status        | requests dimming status | request information       |[  msg_id(H) msg_type=**8** (B)  ]   |    3          |[  msg_id(H) msg_type=**8** (B) dimming(b) ]       | 4                | OK | OK | NO (node invents dimming) |
|neighbours        | requests number of neighbours | request information       | [  msg_id(H) msg_type=**9** (B)  ]   |    3          |[  msg_id(H) msg_type=**9** (B) num_neighbours(I) ]       | 7                | OK | OK | OK |
|rssi        | requests rssi status | request information       |[  msg_id(H) msg_type=10(B)  ]   |    3       |[  msg_id(H) msg_type=**10** (B) rssi(b) ]       | 4       | OK | OK | OK |
|hops        | requests number of hops, the info is in the header of the wirepass message, the node doesn't have to send it | request information       |[  msg_id(H) msg_type=11(B)  ]   |    3       |[  msg_id(H) msg_type=11(B) hops(B) ]       | 4       | OK | OK | OK |
|node status (changed)        | requests all info from node | request information       |[  msg_id(H) msg_type=**12** (B)  ]   |    3       |[ msg_id(H) msg_type=**12**(B) led_status(B) dimming(b) num_neighbours(I) rssi(b) ]| 10      | OK | OK | NO (node invents led_status, dimming, num neigh) |
|send new strategy        | sends new strategy info. Gateway iniciative | sends information       |[  msg_id(H) msg_type=**13** (B) strategy_num(B) num_changes(B) {timestamp(I) dimming (B)}·num_changes  ]   |    5 + 5·num_changess   |[ msg_id(H) msg_type=**13** (B) CRC{ whole payload }(I) ]| 7       | NO | NO | NO |
|error response        | error while processing request | response error       | *whichever request*  |    *n*       |[ msg_id(H) msg_type=**0** (B)  error(B) ]| 4       | NO | OK | NO |

3. Possible node errors include errors 1,3,6,7,9,10,15 from gateway to cloud, plus:
    1. ??? I forgot which errors we could include.

4. Node status metrics
    - **led status** can either be 0 or 1 for closed or open.
    - **dimming** ranges between 0-100 %
    - **neighbours** ranges between 0-10 million
    - **rssi** ranges betweeen -100 and 0 dBm *(0 is the best possible signal)*
    - **hops** ranges betweeen 0 to 256, *(it is the number of jumps a node does to other nodes before reaching a gateway)* this comes implicit in the message from the node to the gateway

5. For each message request, there is an expected response, 
    - **successful request** *expected response* When the node answers with the same original request, this means that the request has been successfully processed by the node and the response should be collected by the sender.
    - **no communication** *missing response* If the request was not received by the node, the sender will receive no response message from the node, thus the gateway will know that the message was not delivered. 
    - **altered communication** *wrong response* If the message was wrongly received and some parameters were distorted in the communication gateway-->node, then the response of the node will be different than the request, and the gateway will be able to identify this and realise the communication was incomplete.
    - **processing problem** *error response*: If the node received the gateway request, but while processing it encountered a problem, it will not respond with the original message. Instead it will send a message type = 0 (default for error), the original message type it received (to check that the error was triggered from the right request and not an altered one) and an extra parameter which will be the type of error it encountered while processing the request

6. Wirepas has some automatic error detection responses, when sending a messages from gateway backend to node, which are coded in the *callback* to the gateway request to the node. These automatic wirepas responses from the node, are way faster than the responses the node can program in its c firmware. In my code this is under the function `on_gateway_answer_callback()` in the script `mqtt_interaction_node_basic`. 

    The gateway error result codes are detailed in the wirepas python library: `wirepas_mesh_messaging` with function: `GatewayResultCode`, the are 30 different error codes, which include:
    - GW_RES_UNKNOWN_ERROR = UNKNOWN_ERROR_CODE
    - GW_RES_OK = OK
    - GW_RES_INTERNAL_ERROR = INTERNAL_ERROR
    - GW_RES_INVALID_SINK_ID = INVALID_SINK_ID
    - GW_RES_INVALID_ROLE = INVALID_ROLE
    - GW_RES_INVALID_NETWORK_ADDRESS = INVALID_NETWORK_ADDRESS
    - GW_RES_INVALID_NETWORK_CHANNEL = INVALID_NETWORK_CHANNEL
    - GW_RES_INVALID_CHANNEL_MAP = INVALID_CHANNEL_MAP
    - GW_RES_INVALID_NETWORK_KEYS = INVALID_NETWORK_KEYS
    - GW_RES_INVALID_AC_RANGE = INVALID_AC_RANGE
    - GW_RES_INVALID_SINK_STATE = INVALID_SINK_STATE
    - GW_RES_INVALID_DEST_ADDRESS = INVALID_DEST_ADDRESS
    - GW_RES_INVALID_DEST_ENDPOINT = INVALID_DEST_ENDPOINT
    - GW_RES_INVALID_SRC_ENDPOINT = INVALID_SRC_ENDPOINT
    - GW_RES_INVALID_QOS = INVALID_QOS
    - ...

1. Different kind of smartec errors
    1. **Driver doesn't respond** When the node receives no confirmation from the driver that it received the node request.
    2. **Node ROM full** No free space to store more information in the node.

2. Message examples:

- Gateway tells node `145` to open the led: The gateway will send to node 145 the following message: 
`144 1` (this message contains the message id "144" and the type of order/message which is 1). Once the message is received and processed by the node, the node will send a response to this call, with the message `144 1` (same message id so that the caller can identify the response in the topic).
- Gateway tells node `145` to put a dimming of 65% to the led: The gateway will send to node 145 the following message: 
` 145 3 65 ` (this message contains the message id "145" and the type of order/message which is 3). Once the message is received and processed by the node, the node will send a response to this call, with the message `145 3 65` (same message id so that the caller can identify the response in the topic).
- Gateway tells node `145` to put a dimming of 65% to the led: The gateway will send to node 145 the following message: 
` 146 3 65 ` (this message contains the message id "145" and the type of order/message which is 3). Once the message is received and processed by the node, the node encounters a problem and the driver doesn't respod to the node. Then the nodel will send the *errors response* message `146 0 1`


### Node requests to gateway

1. Node requests to her gateway. 
2. Message type: The request is specified in the **call** columns and the response to it in the **response** columns:

|message name   | description   | field type    | Call - values | call - bytes  | response - values | response - bytes  | developed by node | developed by gateway | tested the connection | 
|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|:-----------------:|:-----------------:|:-----------------:|:-----------------:|:-----------------:|
|GetTime     | get time from gateway  | request information       |[  msg_id(H) msg_type= **201** (B) ]    |    3          |[  msg_id(H) msg_type= **201** (B) time(I)]        | 7 |  OK | OK | NO |
|Alarm          | sends an alarm        | send information       |[  msg_id(H) msg_type= **202** (B) alarm(B)]   |    4          |[  msg_id(H) msg_type= **202** B) alarm(B)]       | 4                | NO | OK | NO |
|current & voltage     | send metrics *when there are changes* in current or voltage  | send information       |[  msg_id(H) msg_type=**203** (B) voltage(H) current(H) change_type(B)]   |    8          |[  msg_id(H) msg_type=**203** (B) CRC{ voltage current} change_type}(I)]       | 7                | NO | just response | NO |
|electrical parameters     | electrical parameters  | send information  *when there are changes*     |[  msg_id(H) msg_type=**204** (B) voltage(H) current(H) power(H) power line frequency(B) light_level(B) running_hours(I) ]   |    15          |[  msg_id(H) msg_type=**204** (B) CRC{voltage current power freq light hours}(I) ]       | 7                | NO | just response | NO |
|Solar panel metrics     | extra solar consumption metrics  | send information   *when there are changes*    |[  msg_id(H) msg_type=**205** (B) charge(H) production(H)  ]   |    7         |[  msg_id(H) msg_type=**205** (B) CRC{charge production}(I) ]       | 7     |  NO | just response | NO |
|node status       | triggers when there is a change in the electrical parameters | sends information       |[ msg_id(H) msg_type=**206** (B) led_status(B) dimming(b) num_neighbours(I) rssi(b)  ]| 10     |[ msg_id(H) msg_type=**206** (B) CRC{led_status dimming num_neighbours rssi}(I) ]| 7       | OK (invents values) | just response | NO |
|new node (new)       | first message sent by a node | sends information       |[ msg_id(H) msg_type=**207** (B)  ]| 3     |[ msg_id(H) msg_type=**207** (B) ]| 3   | NO | NO | NO |

Explanation of message fields:

1. The **time** is sent in seconds since Jan 1, 1970, 00:00:00. If we use 4 bytes we can send up to 136 years of different times, so until 2106. If we use 8 bytes we could send up to more tha 100 millions years of different times. We will just use 4 bytes then for the time being.

2. Possible alarm types:
    1. **Too much voltage** when voltage is bigger than it should be
    2. **Too much reactive energy** when reactive energy is too much. *Low power factor*
    3. **low power charge** (for solar luminaires)
    4. **0 production for a day** (for solar luminaires)
    5. **0 electric consumption on start** there should be some consumption if lamp is on
    6. **consumption while inactive** there shouldn't be if lamp is off
    7. **no communication with driver** if node can't communicate to driver, something is off
    8. **higher frecuency than expected** if frecuency exceeds the limit

3. Electrical parameters:
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
4. Electrical parameters computed from the previous ones
    1. *Power factor* = power/(voltage*current) tells the ammount of lost energy in the luminaire
    2. *power consumption* = power*hours
    3. *reactive power* = power - voltage*current

5. Solar pannels extra metrics (to be defined)
    1. **battery charge** (we don't know the units or range of values of this yet)
    2. **solar production** (mili watts) 0-60000 (2 bytes)

6. Possible errors: Since the Gateway *is higher in control hierarchy* than the node, it doesn't make sense for the gateway to send an error message to the node in case its petition couldn't be processed.

7. Note: Due to the limit of 256Mb, and the fact that each *node id* needs *8 bytes* to be properly encoded, we can't send more than 3 bytes of node ids. Therefore, to avoid sending more than that, we restricted the ammount of node ids to be sent in a single message, to *2 bytes* or 65535.

## Cloud messaging

The same idea applies in the global setting of 1 cloud with her respectives gateways connected to it. Explained in the document: *"Communication_protocols_cloud_to_gateway.md"* 

If using doxygen or the browser, navigate back to the *main page* here -> [*"Communications summary"*](index.html)