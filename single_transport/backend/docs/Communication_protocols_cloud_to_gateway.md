# Communication protocols between Cloud and Gateway



- [Communication protocols between Cloud and Gateway](#communication-protocols-between-cloud-and-gateway)
  - [Introduction](#introduction)
  - [MQTT topics](#mqtt-topics)
  - [Message content](#message-content)
    - [Explanation of the message fields:](#explanation-of-the-message-fields)
    - [Cloud requests to node](#cloud-requests-to-node)
    - [Possible errors](#possible-errors)
    - [Cloud requests to gateway](#cloud-requests-to-gateway)
    - [Gateway requests/events to the cloud](#gateway-requestsevents-to-the-cloud)
  - [Local messaging](#local-messaging)

## Introduction

In this file we explain the basic theory in the communications between the main cloud backend and the local backends of each gateway. We will:

1. Define a list of mqtt topics that will organise the route of each message
2. Define the content of each message, and where it has to be sent (which mqtt topic)



## MQTT topics

We will use the following mqtt topics

1. Cloud requests to gateways and nodes:

    - `cl-req/n/<node_id>` : (commands to nodes) the cloud-backend will make requests on this topic. The gateway that has unders its control the `<node_id>` in particular, is responsible for subscribing to this topic in order to receive all related messages. Messages sent here include direct commands of "ON", "OFF", "DIMMING" aimed at a specific node.
    - `cl-req/gw/<gateway_id>` : (information about the nodes) the cloud-backend will make requests on this topic. Each gateway is responsible for subscribing to this topic using its own id. These are the requests made to a gateway in particular. Messages here can include to request all connected nodes to the gateway for instance.

2. Gateway responses to cloud requests:

    - `gw-res/n/<node_id>` : (response from gw) here the gateway publishes the result of a cloud request to a specific node.
    - `gw-res/gw/<gateway_id>` : (response from gw) here the gateway publishes the result of a cloud request to a specific gateway

3. Gateway requests/send information to the cloud:
   
    - `gw-req/gw-init/`: (message from gw) a gateway sends its *alive* signal to this mqtt topic, for the cloud to know. 
    - `gw-req/gw/<gateway_id>` : (message from gw) a gateway publishes requests to the cloud here that don't have a prior request from the cloud

4. Cloud responses to gateway requests:

    - `cl-res/gw/<gateway_id>` : (response from cloud) after a gateway communicated something to the cloud, she expects a confirmation response, which indicates if the communication was received and the required task performed. This is the topic where the cloud sends the response.

## Message content

Here we describe the content of each message sent to each machine. The information includes the values sent, a short description, the number of bytes, and the information contained in each byte of the message.

Due to the limitation of **256MB** put on a MQTT message (http://www.steves-internet-guide.com/mqtt-broker-message-restrictions/), the maximum ammount of bytes in a message payload is around **268435455 bytes**, which limits the payload or number of nodes that can be added in a single message in some of the cases below. 

Some notes on the MQTT messages:

1. The `mosquitto_pub ` command sends the message payload in string only, so writing the *payload* in bytes and sending it as bytes via MQTT, will be read as *string* and therefore will use way more bytes than actually sent. The solution is to convert each byte into a character


### Explanation of the message fields:

- The first term is the *message id* and has 2 bytes (H - unsigned long int)
- The second term is the *message type*. We only use 1 byte for this, therefore we have 256 different message types to use. In the gateway-backend to node communication we reserved the values 1-128 for gateway messages to node, and the numbers 129 to 255 for node messages to gateway. However, since each type of message has its own MQTT topic, this distinction is not necessary anymore, and all messages type can be encoded starting by 1 in each case.
- the third to the last term are *message arguments* that depend on the specific message type. Some messages have more arguments, some don't have any.
-  Each value of the message is encoded according to the format of the reference https://docs.python.org/3/library/struct.html. Each value must therefore be encoded in either **1 byte** (B,b), **2 bytes**(H), **4 bytes**(i,I) or **8 bytes**(q,Q) to be platform independent. 
- For more information on the mqtt packet format check https://openlabpro.com/guide/mqtt-packet-format/

### Cloud requests to node

1. Cloud requests to a single node, published on topic `cl-req/n/<node_id>`.
2. Message type: The request is specified in the **call** columns and the response to it in the **response** columns:

|message name   | description   | field type    | Call - values | call - bytes  | response - values | response - bytes  | developed by cloud | developed by gateway | tested the connection | 
|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|:-----------------:|:-----------------:|:-------------:|:-----------------:|:-----------------:|
|led on         | turn led on   | send action       |[  msg_id(H) msg_type= **1** (B) ]    |    3          |[  msg_id(H) msg_type= **1** (B) ]        | 3                 | OK | OK | OK |
|led off        | switch led off| send action       |[  msg_id(H) msg_type= **2** (B) ]   |    3          |[  msg_id(H) msg_type= **2** (B) ]       | 3                | OK | OK | OK |
|dimming        | set dimming for led| send action       |[  msg_id(H) msg_type= **3** (B) dimming(b) ]   |    4          |[  msg_id(H) msg_type= **3** (B) dimming(b) ]       | 4                | OK | OK | OK |
|blink        | start blinking| send action       | [ msg_id(H) msg_type= **4** (B) ]   |    3          |[  msg_id(H) msg_type= **4** (B) ]       | 3                | OK | OK | OK |
|strategy        | send a lighting strategy| send action       |[  msg_id(H) msg_type= **5** (B) strategy(B) ]   |    4          |[  msg_id(H) msg_type= **5** (B) strategy(B) ]       | 4                | OK | OK | node answers with strategy 21 always |
|echo        | requests the  node to run an echo command | request information       | [  msg_id(H) msg_type= **6** (B) ]   |    3          |[  msg_id(H) msg_type= **6** (B) traveltime(I) ]       | 7                | OK | OK | OK |
|led status        | requests led status | request information       |[  msg_id(H) msg_type= **7** (B) ]   |    3          |[  msg_id(H) msg_type= **7** (B) let_status(B) ]       | 4        | OK | OK | OK (node invents value)|
|dimming status        | requests dimming status | request information       |[  msg_id(H) msg_type= **8** (B)  ]   |    3          |[  msg_id(H) msg_type= **8** (B) dimming(b) ]       | 4                | OK | OK | OK |
|neighbours        | requests number of neighbours | request information       | [  msg_id(H) msg_type= **9** (B)  ]   |    3          |[  msg_id(H) msg_type= **9** (B) num_neighbours(I) ]       | 7                | OK | OK | OK |
|rssi        | requests rssi status | request information       |[  msg_id(H) msg_type= **10** (B)  ]   |    3       |[  msg_id(H) msg_type= **10** (B) rssi(b) ]       | 4       | OK | OK | OK |
|hops        | requests number of hops, this request is answered by the gateway, not tunneled to the node | request information       |[  msg_id(H) msg_type= **11** (B)  ]   |    3       |[  msg_id(H) msg_type= **11** (B) hops(B) ]       | 4       | OK | OK | OK |
|node status        | requests all info from node | request information       |[  msg_id(H) msg_type= **12** (B)  ]   |    3       |[ msg_id(H) msg_type= **12** (B) led_status(B) dimming(b) num_neighbours(I) rssi(b) hops(B)  ]| 11      | OK | OK | OK but(node invents led_status and dimming) |
|send new strategy        | sends new strategy info. Gateway iniciative | sends information       |[  msg_id(H) msg_type=**13** (B) strategy_num(B) num_changes(B) {timestamp(I) dimming (B)}·num_changes  ]   |    5 + 5·num_changes       |[ msg_id(H) msg_type=**13** (B) CRC{ whole payload }(I) ]| 7       | NO | NO | NO |
|node software version | asks for node stack & app version | request information       |[  msg_id(H) msg_type=**14** (B) ]   |    3       |[ msg_id(H) msg_type=**14** (B) version(BBBB BBBB) ]| 11       | NO | OK | NO |
|error response        | error while processing request | response error       | *whichever request*  |    *n*       |[ msg_id(H) msg_type= **0** (B) error(B) ]| 4       | OK | OK | OK |

1. Possible errors, described in the next section

2. Description of some commands:
    14. *Ask for node version* Should return a message payload that contains he *version* parameter. This parameter *version* has 8 bytes, the first 4 bytes correspond to the version of the stack: *MAJOR.MINOR.REVISION.BUILDNUMBER*. The next 4 bytes correspond to the *MAJOR.MINOR.REVISION.BUILDNUMBER* for the app that we installed into the node.

3. Doubts about our design:
   1. If node is already on, can a cloud send another led on command? Does the cloud have to check the database first? Does the gateway have to send it to the node anyway and then give an error message to the cloud?
   2. Who is gonna connect to the cloud? all the lamp posts in the world?
   3. How many lamp posts does Salvi have in the world? According to > https://cities-today.com/a-quarter-of-streetlights-could-be-smart-by-2030/ there will be around 361 million street light in the world. At most 622 million if we add tunnel lights, and stadium lights.
   4. How are we going to choose the msg id? do we identify it with the node? If so, do we keep track of the last message id sent, per node? or not? I can think of 3 ways of doing it:
      1. Choose a message id of 8 bytes, and update it in general -> makes the message heavier
      2. Choose a message id of 2 bytes, and update it for each node separately -> a lot of database and CPU consumption
      3. Invent a random message id of 2 bytes, and update it in general -> the probabilities that the same node will repeat the message id are 2.3*10^-10 (0.00000000002) so it will need to send 65000 messages before it can be repeated.
      4. **make front end block** new messages to the same nnode, until the response is received.

4. The gateway answers to this cloud request by publishing the response on topic `gw-res/n/<node_id>`
5. Message examples:

- Cloud tells node 145 to open the led: The Cloud will publish on topic `cl-req/n/145` the following message: 
`500 1` (this message contains the message id "500" and the type of order/message which is also 1). Once the message is received and processed by the gateway, the gateway will send it to the node and publish a response to this call, at topic `gw-res/n/145` with the message `500 1` (same message id so that the caller can identify the response in the topic).
- Cloud tells node 145 to turn off the led: The Cloud will publish topic `cl-req/n/145` the following message:: 
`501 2` (this message contains the message id "501" and the type of order/message which is 2). If the gateway receives the message it will publish a response on topic `gw-res/n/145` with message payload: `501 2`.
- Cloud tells node 145 to set a dimming of 66%: The Cloud will publish topic `cl-req/n/145` the following message:: 
`502 3 66` (this message contains the message id "502" and the type of order/message which is 3, and includes the dimming of 66%). The response will be published at topic `gw-res/n/145` with message payload: `502 3 66`.
- Cloud tells node 145 to set a dimming of 20%: The Cloud will publish topic `cl-req/n/145` the following message:: 
`503 3 20` (this message contains the message id "503" and the type of order/message which is 3, and includes the dimming of 20%). Now the node encounters an error in which it can't detect the driver and then it gives a response that will be published at topic `gw-res/n/145` with message payload: `503 0 1`.

### Possible errors
    1. **Driver doesn't respond** The request was processed from gateway to node, but the driver seems to not operate as expected.
    2. **Node doesn't respond** The gateway can't establish a connection with the desired node.
    3. **Node has ROM full** The node receives the message but can't store more information into its static memory.
    4. **Gateway has ROM full** The gateway can't store the required information in its static memory.
    5. **Gateway error while connecting to local database** The gateway tried to connect to the database but couldn't.
    6. **incorrect message length** The gateway tried to connect to the database but couldn't.
    7. **parameters out of range** Some of the parameters sent are not in the expected range of values. i.e. when a dimming of 129% is sent. Dimming should be between 0 and 100.
    8. **node not in gateway** There is a node not in the gateway that the cloud wanted the gateway to modify
    9. **invalid CRC** The CRC received on the response doesn't match the original message sent from the gateway
    10. **Strategy not found** The strategy sent is not in the gateway database
    11. **error while updating gateway database**
    12. **error while reading gateway database** The database could not be read
    13. **error while updating gateway software** The Gateway tried to update, but the operation wasn't successful
    14. **error in tunneling cloud > node** The tunneling step after receiving the cloud message, didn't go as expected
    15. **Invalid message type** The message type sent is not recognized
    16. **Message payload not in bytes** The message payload received is not in bytes. It should be in bytes to be processed properly
    17. **Invalid message origin (mqtt topic)** The MQTT topic is wrong or not the expected one.
    18. **Couldn't update nodes (OTAP)** The OTAP request sent to the gateway, didn't go as expected

### Cloud requests to gateway

1. Cloud requests to a specific gateway, published on topic `cl-req/gw/<gateway_id>`. The Gateway will take the request and make a broadcast to all nodes. That's to say, according to wirepass this is done on address "0xFFFFFFFF". The gateway response to this cloud request will contain the node address: "all". However, the *cloud* must specify the **cleiint id** of the nodes that we want to open. The Gateway will broadcast to all "0xFFFFFFFF" if all nodes of the gateway belong to the same client, but will send a list otherwise.
2. Message type: The request is specified in the **call** columns and the response to it in the **response** columns:

|message name   | description   | field type    | Call - values | call - bytes  | response - values | response - bytes  |  max nodes | developed by cloud | developed by gateway | tested the connection | 
|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|:-----------------:|:-----------------:|:-----------------:|:-----------------:|:-----------------:|:-----------------:|
|~~led on all~~      | ~~turn on all nodes' led~~ (DELETED) | ~~send action~~       |~~[  msg_id(H) msg_type= **1** (B) client_id(I) ]~~    |   ~~7~~        | ~~[  msg_id(H) msg_type= **1** (B) client_id(I) ]~~        | ~~7~~  |   | ~~NO~~ | ~~NO~~ | ~~NO~~ |
|~~led off all~~     | ~~turn off all nodes' led~~ (DELETED) | ~~send action~~       | ~~[  msg_id(H) msg_type= **2** (B) client_id(I) ]~~   |    ~~7~~          |~~[  msg_id(H) msg_type= **2** (B) client_id(I) ]~~       | ~~7~~                |     | ~~NO~~ | ~~NO~~ | ~~NO~~ |
|~~dimming all~~     | ~~set dimming to all nodes~~ (DELETED) | ~~send action~~       |~~[  msg_id(H) msg_type= **3** (B) client_id(I) dimming(b) ]~~   |    ~~8~~          | ~~[  msg_id(H) msg_type= **3** (B) client_id(I) dimming(b) ]~~       | ~~8~~                |    | ~~NO~~ | ~~NO~~ | ~~NO~~ |
|~~node status~~     | ~~get status of nodes connected to gw~~ (DELETED) | ~~request information~~       |~~[  msg_id(H) msg_type= **5** (B) client_id(I) ]~~    |     ~~7~~       |~~[  msg_id(H) msg_type= **5** (B) client_id(I) num_nodes(H) { node_ids(Q) led_state(B) dimming(b) num_neighb(I) rssi(b) hops(B) }*num_nodes]~~        | ~~9 + 16·num_nodes~~              |   ~~4931 (108500 bytes)~~ | ~~NO~~ | ~~NO~~ | ~~NO~~ |
|node list     | get nodes connected to gw  | request information       |[  msg_id(H) msg_type= **4** (B) client_id(I) ]    |    7          |[  msg_id(H) msg_type= **4** (B) client_id(I) num_nodes(H) node_ids(Q)*num_nodes]      | 9 + 8·num_nodes              |  13561 (108500 bytes)    | NO | OK (but gw invents them) | NO |
|remove nodes     |  only command that the cloud does automatically |  send action  |[ msg_id(H) msg_type= **6** (B)  num_nodes(H) node_ids(Q)*num_nodes ] |    5  + 8·num_nodes        |[ msg_id(H) msg_type= **6** (B)   CRC{ num_nodes node_ids) }(I)  ]    | 7            |  | NO | OK (but gw invents them) | NO |
|update gateway*     |  update gateway software from github  *takes around 30sec to complete* |  send action  |[ msg_id(H) msg_type= **7** (B) ] |    3        |[ msg_id(H) msg_type= **7** (B)    ]    | 3            |  | NO | OK | NO |
|update nodes*     |  update nodes with the gateway scratchpad *takes around 3min to complete* |  send action  |[ msg_id(H) msg_type= **8** (B) ] |    3        |[ msg_id(H) msg_type= **8** (B)    ]    | 3            |  | NO | OK | NO |
|get gw version*     |  get the gateway version |  request info  |[ msg_id(H) msg_type= **9** (B) ] |    3        |[ msg_id(H) msg_type= **9** (B) version(BBBB)    ]    | 7            |  | NO | NO | NO |
|error response        | error while processing request | response error       | *whichever request*  |    *n*       |[ msg_id(H) msg_type= **0** (B)  error(B) ]| 4       |  | OK | OK | OK |

1. Possible errors

    1. **Gateway has ROM full** The gateway can't store the required information in its static memory.
    2. **Gateway error while connecting to local database** The gateway tried to connect to the database but couldn't.

2. Possible device values for **update software** command:
   1. Update gateway software via Github
   2. Update node software, by downloading the scratchpad.otap file from github, and then send it to the sink(s) and propagate to nodes via OTAP.

3. The gateway answers to this cloud request by publishing the response on topic `gw-res/gw/<gateway_id>` 
4. Note: Due to the limit of 256Mb, and the fact that each *node id* needs *8 bytes* to be properly encoded, we can't send more than 3 bytes of node ids. Therefore, to avoid sending more than that, we restricted the ammount of node ids to be sent in a single message, to *2 bytes* or 65535.

5. Examples
    - **node status** response *(message type = 5)* `payload = pack("<HBHQBbIiIQBbIiI",12132,5,2,134,1,55,3,-67,2,135,1,80,0,-117,5)`

### Gateway requests/events to the cloud

1. Gateway event messages (as different from response messages) to the Cloud, published on topic `gw-req/gw/<gateway_id>`. Message type:
2. Message type: The request is specified in the **call** columns and the response to it in the **response** columns:

|message name   | description   | trigger | field type    | Call - values | call - bytes  | response - values | response - bytes  | developed by cloud | developed by gateway | tested the connection | 
|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|:-----------------:|:-----------------:|:-------------:|:-----------------:|:-----------------:|
|alive          | echo signal to send ID to mqtt topic `gw-req/gw-init` | when gw starts  | sends information       |[ msg_id(H) msg_type= **1** (B) gw_id(Q) ]     |   11         |[ msg_id(H) msg_type= **1** (B) gw_id(Q)]       |  11               | NO | NO | NO |
|add nodes       | tells which nodes have been added to this gateway recently | when a new node appears | sends information       |[ msg_id(H) msg_type= **2** (B)  num_nodes(H) node_ids(Q)*num_nodes ] |    5  + 8·num_nodes        |[ msg_id(H) msg_type= **2** (B)   CRC{ num_nodes node_ids) }(I)  ]    | 7            | OK | OK | YES (gw fakes nodes, cloud fakes crc) | 
| not seen nodes       | tells which nodes aren't seen anymore in this gateway recently | sends information      |[ msg_id(H) msg_type= **3** (B)  num_nodes(H) node_ids(Q)*num_nodes ] |    5  + 8·num_nodes        |    | [ msg_id(H) msg_type= **3** (B)   CRC{ num_nodes node_ids) }(I)  ]    | 7           | OK | OK | YES (gw fakes nodes, cloud fakes crc) |    
|node status list     | sends status of the selected nodes| sends information, (periodic)?       | [  msg_id(H) msg_type= **4** (B) num_nodes(H) { node_ids(Q) led_state(B) dimming(b) num_neighb(I) rssi(b) hops(B) }*num_nodes]        | 5 + 16·num_nodes     |[ msg_id(H) msg_type= **4** (B)   CRC{ all arguments }(I)  ]    |  7          | OK | OK | YES(gw fakes nodes, cloud fakes crc) |
|alarm       | sends alarm to cloud concerning several nodes| sends information       | [ msg_id(H) msg_type= **5** (B)  alarm_type(B) num_nodes(H) node_ids(Q)*num_nodes ] |    6+8·num_nodes  |[ msg_id(H) msg_type= **5** (B)  alarm_type(B) CRC {all arguments}(I) }  ]    | 8            | OK | OK | YES (gw fakes alarm & nodes, cloud fakes crc) |
|electric parameters list       | sends consumptions to cloud | sends information, periodic    | [ msg_id(H) msg_type= **6** (B)   num_nodes(H) { node_ids(Q) voltage(H) current(H) power(H) frequency(B) light_level(B) running_hours(I)}*num_nodes ] |   5 + 20·num_nodes  |[ msg_id(H) msg_type= **6** (B)   CRC{ all arguments }(I) ]    | 7            | OK | OK | YES(gw fakes parameters, cloud fakes crc) |
|error response        | error while processing request | response error       | *whichever request*  |    *n*       |[ msg_id(H) msg_type= **0** (B)  error(B) ]| 4       |  | NO | NO | NO |

3. **Consumption** metrics (also explained in the *"Communication_protocols_gateway_to_node.md"* file at *#node requests to gateway*)
    1. **voltage** (volts) 0-300 (2 bytes)
    2. **current** (amperes) 0-600 (2 bytes)
    3. **power** (watts) 0-600 (2 bytes)
    4. **frequency** (Hz) 0-180 (1 byte)
    5. **light level %** (0-100) (1 byte)
    6. **running hours** (in minutes, for 8100 years) (4 bytes)
    


4. Possible errors: Since the Cloud *is higher in control hierarchy* than the gateway, it doesn't make sense for the cloud to send an error message to the gateway in case its petition couldn't be processed.


5. The cloud answers to this gateway request by publishing the response on topic `cl-res/gw/<gateway_id>` **as soon as it receives the request**. Since the Cloud *is higher in hierarchy* than the gateway, it doesn't make sense to wait and inform a gateway of a possible cloud error.

6. **Examples**
    - on **alarm with node list** *(message type = 133)* an example of payload could be `payload = pack("<HBBHQQQ",12132,133,2,3,141,142,144)` where we have 3 nodes, with ids 141, 142, 144, and an alarm of value **2**.

    - **consums** list example *(message type = 134)* an example of payload could be `payload = pack("<HBHQHHHBBIQHHHBBIQHHHBBI",12132,134,3,141,220, 340, 460, 40, 80, 6500300,142,220, 440, 160, 40, 20, 6506600,144, 220, 290, 190, 40, 28, 6502400)`

7. **Double check** for the command has been received properly:
    - For **add nodes** make the cloud send an echo to each node that has been added.
    - For **not seen nodes**  check that the gateway indeed doesn't have it or some other gateway has it.
## Local messaging

The same idea applies in the local setting of 1 gateway with her respectives nodes connected to it. Explained in the document: *"Communication_protocols_gateway_to_node.md"*

If using doxygen or the browser, navigate back to the *main page* here -> [*"Communications summary"*](index.html)

Random math to try out Mathjax:

When $a \ne 0$, there are two solutions to $\left((ax^2 + bx) + c = 0\right)$ and they are 
$$ x = {-b \pm \sqrt{b^2-4ac} \over 2a} $$