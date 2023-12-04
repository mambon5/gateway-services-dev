# Communication protocols between Cloud <--> Gateway <--> Nodes (mesh network)



1. [Introduction. ](#introduction)
2. [Request<-->response messaging model ](#request--response-messaging-model)
    - [Request flows](#request-flows)
    - [Chained responses](#chained-responses)
    - [Who has to report the processing errors?](#who-has-to-report-the-processing-errors)
    - [Error handling](#error-handling)
3. [Message content](#message-content)
    - [Weight and format of the message fields](#weight-and-format-of-the-message-fields)
4. [Local messaging. ](#local-messaging)
5. [Cloud messaging. ](#cloud-messaging)

## Introduction

In this file we explain the basic functionality of the communications between the local backend of a gateway, the mesh networks aka the nodes and the cloud. **cloud <--> gateway <--> node** We will:

1. Explain the **request-response** messaging model 
2. When has the response to be sent?
3. The different control **hierarchy** of each entity involved (or just hierarchy).
4. Short explanation on the message content in general.
5. Where to find detailed information on the different message contents.

## Request<-->response messaging model:

We have different kind of messages depending on the communication. 
- It can be: 1. gateway <--> node interaction or 2. cloud <--> gateway interaction.
- There is always a **sender** that sends the message *request*, and a **receiver** and receives the message.
- The *sender* always waits to see a response up to certain ammount of time. It creates a thread if necessary to not obstruct other work that the CPU might already be doing.
- The *receiver* **must** send a *response* once it receives and processes a request. The response can indicate either that:
    1. The message has not been processed due to an error -> we call this a **processing error**.
    2. The message has been processed successfully.
- The abscense of a reponse, tells the sender that the message has not been received, then the sender can act accordingly depending on the case.

### Request flows:

We have the following different request flows. A **flow** is the direction and sense in which the request is sent. It consists of the receiver and the sender.

1. **cloud --> node** & its response. Msg types include: 1-12, 0
2. **cloud --> gateway** & its response. Msg types included: 1-5, 0
3. **gateway --> cloud** & its response. Msg types include: 129-134
4. **gateway --> node** & its response. Msg types include: 1-12, 0
5. **node --> gateway** & its response Msg types include: 201-205

### Chained responses

In some cases in which 2 interactions are related via a tunnel, it will be necessary to wait for the first response to come to the gateway, before sending the second response to the cloud. In other cases, this won't be necessary. We give now the different possibilities:

1. In the messages of the request flow 1. **cloud --> gateway --> node** the gateway will eventually send a message request to the node, who will hopefully response. Once the gateway obtained its response from the node, it will be the right time to analyse the response and send a corresponding response to the original cloud request. *We cannot send the response to the cloud before we received and analysed the node response to the gateway request*

2. In messages of the request flow **node --> gateway --> cloud** such as a Node alarm, it won't be necessary to chain the responses and wait for the cloud response to the gateway request, before sending the response to the node. The node is in a *lower control hierarchy* level than the cloud, thus it is not necessary that it knows whether the cloud received the response or not. It all needs to know that the gateway received it, for the gateway will be then responsible of ensuring that the cloud receives it.

3. In other interactions where no tunneling is done, there is no need to use any *chained response*

### Who has to report the processing errors?

The short answer is: the entity that is lower in **hierarchy** of the two interlocutors. The control hierarchy is the following, from higher to lower hierarchy:

- Front end app
- Cloud platform
- Gateway
- Node
- lamp driver

To be precise, this is how a *request<-->response* with an *error* must happen:

3. If the receiving end is lower in *hierarchy* than the sender, then the request is received and an error occurs during this processing, an **error response** will be sent to the sender, informing it of the problem.
4. However, if the receiver is *higher* in hierarchy than the sender, then once a request is received if there is an error in the processing no error will be sent back to the sender.

This is because it doesn't make sense to let a sender which is lower in heirarchy know about it. The control flows from lower to higher control hierarchy, and thus all the rellvant information on how the network is performing should flow upwards (the ultimate highest control hierarchy entity would be the customer or a human) and not downards.

### Retry mechanisms

There is no need to implement any retry mechanism for any of the messages sent from any of the entities *cloud, gateway, node*. If a message is not received from:

1. **front --> cloud --> gateway --> node** then let the user press the button and send it again. Regardless of which message it is.
2. **node --> gateway** they are going to be sent with QOS = 1 in MQTT, so we expect to receive the message. However, if the node doesn't received the 
    -  **alarm** or **get_time** or **node status** or **electric parameters** 4 retries with increasing waiting times if QoS 1 doesn't guarantee delivery. Starts with a waiting time of 3s.
3. **gateway --> cloud** for all messages, 4 retries with increasing waiting times if QoS 1 doesn't guarantee delivery. Starts with a waiting time of 3s.
4. **front --> gateway** the same as in *front --> cloud --> gateway --> nodes* we will let the user press the button again
5. **cloud --> gateway** in the *remove nodes* message, we need a response, so apply the same scheme of 4 retries with increasing waiting times if QoS 1 doesn't guarantee delivery. Starts with a waiting time of 3s.
6. **gateway --> node** The only messages from gateway iniciative to node are:
    - *echo* (to see if node is still alive) retry 2 times for instance, after that, consider node is dead. Also do this command periodically. Or should the node do it?
    - *send new strategy*. If the strategy is not received, we should resend it to the node, no?


### Error handling

What to do when there is a communication error?

1. There is no response to a previous request

    This case is covered in the section of [retry mechanisms](#retry-mechanisms). If no answer is provided to a specific request, another request will have to be made.

2. Incorrect message length
    
    This is already handled by the gateway script. If too many or too few bytes are passed, compared to the message type, the gateway program will detect it automatically and output a log message saying so. The gateway listening thread will not crash and will keep listening to new messages.

    - If an incoming request has the wrong message length, respond with error code 6.
    - If the response to a gateway request has the wrong message length, resend command to node or cloud (whoever responded)

3. Wrong parameter values

    What to do if a dimming value is incorrect? or the Rssi? or the passed number of neighbours? The gateway should be able to understand what is the right range for some of the values. This could be detected early in parsing. We could make the gateway respond with an error code *parameter value not in accepted range* to indicate the node or cloud of this. These can be some of the situations:

        1. A dimming of more than 100%
        2. A led value that is not either 0 or 1
        3. An alarm value that is not in the list
        4. A negative *travel time* for an echo response

    - same as with incorrect message length.

4. What if the gateway crashes and stops listening? 

    We should enable a restart mode to allow the gateway to reboot in case it stops its listening thread for any reason. No? Yes, use pm2.



5. What if a value can't be stored in the database?

    It probably means that the query has something wrong with it, we could program to just log out an error like "couldn't access the local SQL database/table" and send an alarm to the cloud?

    - yes, send alarm to cloud
    - save information temporarily in a text file
    - resend the data from the node to the cloud directly

    - respond with error code **5**.

6. Sink doesn't work.

    - (to be done in the future) we could subscribe to MQTT topic *gw-event/status/<gw_id>* in order to detect if the sink disconnects

7. MQTT server goes down

    - try to restart mosquitto again.




## Message content

Here we describe the general content of each message sent to each machine. The information of the message generally includes:
1. A temporarily unique **message id**, that will identify the message with its response, uniquely, for a short period of time. 
2. The **message type** which tells most of the information to the receiver. Depending on the value of the *message type* the receiver will understand that it has to either open a led, set some dimming, send information over its electrical consumption in the last hour, or any other circumstance.
3. **additional arguments** that are needed to process the request. They vary depending on the *message type+. If message type indicates set up a dimming, then an additional argument would be the dimming value for instance.

The message content completely depends on the 2 entities that are exchanging informatio.

**Note:** Notice that wirepass transforms the payload we send, and adds extra information such as 
- destination_address
- source_endpoint
- destination_endpoint
- qos
- payload *<-- the initial payload*
- initial_delay_ms *(if initial_delay_ms > 0)*
- is_unack_csma_ca *(if is_unack_csma_ca is True)*
- hop_limit *(if hop_limit > 0)*
as described already in the documment *Communication_protocols_gateway_to_node.md*. For instance, if we just want to send a "send action" command from gateway to node, containing a message id of *1022* and a message type of *3* (3 bytes in total), the wirepass libraries end up sending around 33 bytes of message. Thus it appends around 30 bytes to each sent message in order to use the wirepass technology and ensure its optimal distribution.

### Weight and format of the message fields:

- The *message id*  has 2 bytes (H - unsigned long int)
- The *message type* only uses 1 byte, therefore we have 256 different message types to use. In the gateway-backend to node communication we reserved the values 1-128 for gateway messages to node, and the numbers 129 to 255 for node messages to gateway. However, in the gateway to cloud communications since each type of message has its own MQTT topic, this distinction is not necessary anymore, and all message types can be encoded starting by 1 in each case.
- The third to the last term are the different *message arguments* that vary depending on the different message types. Some messages have more arguments, some don't have any.
- Each value of the message is encoded according to the format of the reference https://docs.python.org/3/library/struct.html. Each value must therefore be encoded in either **1 byte** (B,b), **2 bytes**(h,H), **4 bytes**(i,I) or **8 bytes**(q,Q) to be platform independent. The lower case denotes a signed integer, while the upper case denotes an positive integer.

- Limit of mosquitto MQTT message weight: **108500 bytes** *(tested by Alice and Romà on cloud MQTT broker)*. 

## Local messaging

The details of the messages sent between gateway and node are explained in the document: [*"Communication_protocols_gateway_to_node.md"*](md_backend_Communication_protocols_gateway_to_node.html)

## Cloud messaging

The details of the messages sent between gateway and node are explained in the document: [*"Communication_protocols_cloud_to_node"*](md_backend_Communication_protocols_cloud_to_gateway.html) 

