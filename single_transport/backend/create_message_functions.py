"""
Script responsible for transforming the information into bytes and creating the message for the desired entity. 

- Once an "interaction mode" is selected, you can choose to create a message
- This script switches between the different MQTT supertopics in order to know which kind of message is desired
- Once a supertopic and message type are chosen, it will call a specific message content function, for message content creation

- Some functions are not for production yet, and they invent or randomly generate the messages, for testing the infrastructure.
"""
import global_vars as gvar
from struct import *
import create_message_cloud as cmsgcloud
import create_message_nodes as cmsgnodes

def get_msg_from_input(msg_id, pubtopic):
    """
    Creates a message based on the user input. Read the user input, and puts all the message information into bytes.
    This function is designed for testing purposes only, won't be called in production.
    
    :param msg_id: message temporary unique identifier (id)
    :type msg_id: int
    :param pubtopic: MQTT topic where we will publish our message (None for gateay to node messaging)
    :type pubtopic: string

    :return:
        :payload (bytes) -- message payload
    
    """
    prefix = "<send_msg_from_input>: "
    pub_supertopic = gvar.get_supertopic(pubtopic)

    data = input("input the type of message and additional fields: ")
    data = data.split(" ")
    try:
        data.remove("")                  # this is done in order to remove any empty elements '' in the array
    except:
        pass
    data = list(map(int, data))
    print(data)
    lenarg = len(data)-1
    print(prefix+"msg_id: " + str(msg_id) + ", msg_type: " + str(data[0]) + " num arguments: " +str(lenarg) + ", type & arguments: " + str(data))

    payload = message_to_bytes(msg_id, data[0], data[1:], pub_supertopic, prefix)

    
    return payload


def message_to_bytes(msg_id, msg_type, args, pub_supertopic, prefix="", msg=None) :
    """It creates the byte payload for delivery. It creates the message payload (in bytes) just using the:
        1. message id
        2. message type
        3. message arguments
        4. publication mqtt topic 
    this message is the one that will be sent.
    We assume that all the necessary arguments have been passed for creating the message.

    :param msg_id: message id 
    :type msg_id: int
    :param msg_type: message type 
    :type msg_type: int
    :param args: arguments that we wish to include in the message 
    :type args: list
    :param pub_supertopic: MQTT super topic where the message is gonig to be published. 
    :type pub_supertopic: string
    :param prefix: string to prepend to all the prints/console logs
    :type prefix: string
    :param msg: messge received class RxMsg, only when creating response messages to a previous request! This field will be *None* for request mode
    :type msg: RxMsg

    :return:
        :payload: *(bytes)* -- generated message payload


    :does:
        In order to encode the message it calls a series of subfunctions depending on the 

            1. Message type
            2. Message destination *(represented by the pubtopic parameter)*
        
        There are a total of 9 types of messages to be created from the gateway (or simulated):

            1. **gateway** response to cloud request to node
            2. **gateway** response to cloud request to gateway
            3. **gateway** request to cloud
            4. **gateway** request to nodes
            5. **gateway** response to nodes
            6. node request to **gateway** (simulated)
            7. cloud request to node (simulated)
            8. cloud request to **gateway** (simulated)
            9. cloud response to **gateway** request (simulated)

       messages 1-5 are the production-time messages that the gateway will indeed create, number 6 simulates the node requests and 7-9 simulate the 
        cloud messages and responses. The last 4 messages are purely for testing that the first 5 gateway messages work as expected.
    """

    prefix = prefix + "msg to bytes > "
    payload = pack(gvar.MSG_PAYLOAD_ENDIANNESS_v2+"HB", msg_id, msg_type)
    timestamp = gvar.get_timestamp()

    print(prefix + "creating message at:" + timestamp)

    # pub_supertopic = gvar.get_supertopic(pubtopic)

    # SEND ERROR MESSAGE (if applicable)
    if msg_type == gvar.MSG_TYPE_ERROR:
        # print(prefix + "error message " + str(args[0]))
        payload = payload + pack(gvar.MSG_PAYLOAD_ENDIANNESS_v2+"B", args[0] )
        # print("{} payload: {}".format(prefix, payload))

    # GATEWAY RESPONSE TO CLOUD REQ TO NODE
    elif pub_supertopic == gvar.GATEWAY_RESPONSE_TO_CLOUD_REQUEST_TO_NODE_MQTT_SUPERTOPIC:
        print(prefix + "gateway response to cloud request to node")

        payload = payload + cmsgcloud.gw_resp_to_cloud_req_to_node(msg_type, args, prefix)               

    # GATEWAY RESPONSE TO CLOUD REQUEST TO GW
    elif pub_supertopic == gvar.GATEWAY_RESPONSE_TO_CLOUD_REQUEST_TO_GATEWAY_MQTT_SUPERTOPIC:
        print(prefix + "gateway response to cloud request to gateway")
        payload = payload + cmsgcloud.gw_resp_to_cloud_req_to_gw(msg_type, args, prefix)              

    # GATEWAY REQUEST TO CLOUD
    elif pub_supertopic == gvar.GATEWAY_REQUEST_TO_CLOUD_MQTT_SUPERTOPIC:
        print(prefix + "gateway request to cloud") 
        payload = payload + cmsgcloud.gw_request_to_cloud(msg_type, args, prefix)               

    # GATEWAY --> NODE MESSAGING
    elif pub_supertopic == None: 
        print(prefix + "gateway to node messaging") 

        # GATEWAY REQUESTS TO NODE
        if msg_type in gvar.MSG_RESPONSE_RECEIVED_FROM_NODES_LIST:
            payload = payload + cmsgnodes.gateway_request_to_nodes(msg_type, args, prefix="")

        # GATEWAY RESPONSE TO NODE
        elif msg_type in gvar.MSG_NODE_REQUESTS_LIST:            
            payload = payload + cmsgnodes.gateway_response_to_nodes(msg, args, prefix)
    
        else :
            print(prefix + "wrong message type")
            return payload

    # delete this case, it is only for testing:

    # NODE REQUEST TO GATEWAY
    elif pub_supertopic == gvar.NODE_REQUEST_TO_GATEWAY_MQTT_SUPERTOPIC:
        
        if msg_type in gvar.MSG_NODE_REQUESTS_LIST:
            payload = payload + cmsgnodes.node_request_to_gateway(msg_type, args, prefix)

    # DELETE THE FOLLOWING THREE CASES AND FUNCTIONS FOR PRODUCTION: (this is just for testing purposes)

    # CLOUD REQUEST TO NODE
    elif pub_supertopic == gvar.CLOUD_REQUEST_TO_NODE_MQTT_SUPERTOPIC:
        print(prefix + "cloud to node message request")
        payload = payload + cmsgcloud.cloud_request_to_node(msg_type, args, prefix)

    # CLOUD REQUEST TO GATEWAY
    elif pub_supertopic == gvar.CLOUD_REQUEST_TO_GATEWAY_MQTT_SUPERTOPIC:
        print(prefix + "cloud to gateway message request")
        payload = payload + cmsgcloud.cloud_request_to_gateway(msg_type, args, prefix) 
        
    # CLOUD RESPONSE TO GATEWAY REQUEST
    elif pub_supertopic == gvar.CLOUD_RESPONSE_TO_GATEWAY_REQUEST_MQTT_SUPERTOPIC:
        print(prefix + "cloud_response_to_gateway_req") 
        payload = payload + cmsgcloud.cloud_resp_to_gateway(msg_type, args, prefix, msg)

    else:
        print(prefix+"error: invalid message origin!")

    return payload
    

