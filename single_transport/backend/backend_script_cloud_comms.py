"""
Main script responsible for handling the gateway communications with the cloud.
Can be called by other scripts, using the function "run_cloud_comunications()" or can be called directly from the terminal shell, if so,
it will display an interactive menu. 

Either way, when calling this script you should select **one** of the following mqtt interaction modes:

    1.  Gateway listens for cloud requests to a specific node
    2.  Gateway listens for cloud requests to the gateway
    3.  Gateway sends a request to the cloud

    To ease the development of all the gateway communication functionalities, I added three extra
    modes that are for development purposes only (not for production) which simulate the 
    behaviour of the cloud. These are:

    4.  Cloud sends a message to a specific node
    5.  Cloud sends a message to a gateway
    6.  Cloud listens for gateway direct requests

   Once a mode is selected, the script will:

    - choose a publication MQTT topic
    - select a subscription MQTT topic
    - create an interaction with the cloud, using the :class:`mqtt_interaction_cloud <mqtt_interaction_cloud.mqtt_interaction_node_main>` class
    
    
    Finally, the following is triggered depending on the interaction mode (listen or send):

    - *for listen modes*: the subscription loop starts
    - *for send modes*: the send message function is called.

    """

# modules and python libraries:

from ast import literal_eval # in order to unstring the str-ed byte code
from struct import *
import global_vars as gvar # import global variables
from mqtt_interaction_cloud import mqtt_interaction_cloud        #import the mqtt interaction class in order to send/receive anything that we need


# Learn about MQTT: https://www.hivemq.com/mqtt-essentials/ 

def set_mqtt_topics(node_id):
    """
    Function that sets the cloud MQTT topics based on the node id.

    :param node_id: id of the node the cloud wishes to send messages to, and we as the gateway wish to hear.
    :type node_id: int

    :returns:
        :list: 
            - **TOPIC_LIST** (*list*) -- list with all the mqtt topics we might subscribe/publish to 
            - **MODE_LIST** (*list*) -- list of all the possible interaction modes with the cloud
    
    :does: Apart from the returned items, this function also declares a total of 12 global variables, which include the different
            interaction modes, as well as the different and possible MQTT topics.
    """
    prefix = "<set mqtt topics> "
    node_id = str(node_id)
    global CLOUD_REQUEST_TO_NODE_MQTT_TOPIC, CLOUD_REQUEST_TO_GATEWAY_MQTT_TOPIC, GATEWAY_RESPONSE_TO_CLOUD_REQUEST_TO_NODE_MQTT_TOPIC,     GATEWAY_RESPONSE_TO_CLOUD_REQUEST_TO_GATEWAY_MQTT_TOPIC,   GATEWAY_REQUEST_TO_CLOUD_MQTT_TOPIC,     CLOUD_RESPONSE_TO_GATEWAY_REQUEST_MQTT_TOPIC
    global GATEWAY_RECEIVE_CLOUD_REQUESTS_TO_NODE_MODE, GATEWAY_RECEIVE_CLOUD_REQUESTS_TO_GATEWAY_MODE, GATEWAY_SEND_CLOUD_REQUESTS_MODE, fake_cloud_node_pub, fake_cloud_gw_pub, fake_cloud_sub

    ## mqtt topics:
    CLOUD_REQUEST_TO_NODE_MQTT_TOPIC=gvar.CLOUD_REQUEST_TO_NODE_MQTT_SUPERTOPIC + node_id
    CLOUD_REQUEST_TO_GATEWAY_MQTT_TOPIC=gvar.CLOUD_REQUEST_TO_GATEWAY_MQTT_SUPERTOPIC + node_id
    GATEWAY_RESPONSE_TO_CLOUD_REQUEST_TO_NODE_MQTT_TOPIC = gvar.GATEWAY_RESPONSE_TO_CLOUD_REQUEST_TO_NODE_MQTT_SUPERTOPIC + node_id
    GATEWAY_RESPONSE_TO_CLOUD_REQUEST_TO_GATEWAY_MQTT_TOPIC = gvar.GATEWAY_RESPONSE_TO_CLOUD_REQUEST_TO_GATEWAY_MQTT_SUPERTOPIC + node_id
    GATEWAY_REQUEST_TO_CLOUD_MQTT_TOPIC= gvar.GATEWAY_REQUEST_TO_CLOUD_MQTT_SUPERTOPIC + node_id
    CLOUD_RESPONSE_TO_GATEWAY_REQUEST_MQTT_TOPIC= gvar.CLOUD_RESPONSE_TO_GATEWAY_REQUEST_MQTT_SUPERTOPIC + node_id

    TOPICS_LIST = [
        CLOUD_REQUEST_TO_NODE_MQTT_TOPIC,
        CLOUD_REQUEST_TO_GATEWAY_MQTT_TOPIC,
        GATEWAY_RESPONSE_TO_CLOUD_REQUEST_TO_NODE_MQTT_TOPIC,
        GATEWAY_RESPONSE_TO_CLOUD_REQUEST_TO_GATEWAY_MQTT_TOPIC,
        GATEWAY_REQUEST_TO_CLOUD_MQTT_TOPIC,
        CLOUD_RESPONSE_TO_GATEWAY_REQUEST_MQTT_TOPIC
        ]

    ## thread modes: 
    GATEWAY_RECEIVE_CLOUD_REQUESTS_TO_NODE_MODE = "gw listener for node messages > "+"RECEIVE FROM: " + CLOUD_REQUEST_TO_NODE_MQTT_TOPIC+" RESPOND_TO: " + GATEWAY_RESPONSE_TO_CLOUD_REQUEST_TO_NODE_MQTT_TOPIC
    GATEWAY_RECEIVE_CLOUD_REQUESTS_TO_GATEWAY_MODE = "gw listener for gateway messages > "+"RECEIVE FROM: " + CLOUD_REQUEST_TO_GATEWAY_MQTT_TOPIC+" RESPOND TO: " + GATEWAY_RESPONSE_TO_CLOUD_REQUEST_TO_GATEWAY_MQTT_TOPIC
    GATEWAY_SEND_CLOUD_REQUESTS_MODE = "gw event sender to cloud > "+"REQUEST TO: "+ GATEWAY_REQUEST_TO_CLOUD_MQTT_TOPIC + " LISTEN FROM: "+CLOUD_RESPONSE_TO_GATEWAY_REQUEST_MQTT_TOPIC

    fake_cloud_node_pub = "fake_cloud_to_node_publisher"
    fake_cloud_gw_pub = "fake_cloud_to_gateway_publisher"
    fake_cloud_sub = "fake_cloud_subscriber_from_gw"

    MODE_LIST = [
        GATEWAY_RECEIVE_CLOUD_REQUESTS_TO_NODE_MODE,
        GATEWAY_RECEIVE_CLOUD_REQUESTS_TO_GATEWAY_MODE, 
        GATEWAY_SEND_CLOUD_REQUESTS_MODE,
        fake_cloud_node_pub,
        fake_cloud_gw_pub,
        fake_cloud_sub]

    return [TOPICS_LIST, MODE_LIST]

def run_cloud_comunications(mode="", wni=None, gw_id = None, sink = None):   
    """
    Starts the gateway communications with the cloud via a global MQTT broker. It allows the  user to select a mode or to supply a
    mode when calling the function, directly. 
    
    :does: It does the following:

    1. Select a cloud interaction mode:
        0. gw listener for node messages
        1. gw listener for gateway messages
        2. gw event sender to cloud
        3. fake_cloud_to_node_publisher
        4. fake_cloud_to_gateway_publisher
        5. fake_cloud_subscriber_from_gw
    
    2. Start a cloud interaction with the corresponding publication and subscription MQTT topics to the global server.

    3. Execute the main mode of the interaction, which can be "listen" or "request" 
        - If mode = "listen" the "self.listen()" function is run
        - Otherwise, if mode = "request" the "inter.send_message()" method is started.
    
    """
    prefix = "<run cloud comm's> "
    [TOPICS_LIST, MODE_LIST] = set_mqtt_topics("<device id>")

    if mode == "":
        # user selects and index of the mqtt mode:
        mode = gvar.display_and_set_interaction_mode( MODE_LIST )
    else :
        # mode index already supplied
        print("input already supplied when calling this function")
             
    device_id = None

    if MODE_LIST[mode] in [
        # if mode selected involves a node (or it simulates the cloud itself), 
        # then ask for that node id and reset the mqtt topics
        GATEWAY_RECEIVE_CLOUD_REQUESTS_TO_NODE_MODE, 
        fake_cloud_node_pub,
        fake_cloud_gw_pub,
        fake_cloud_sub]:
        
        # device_id = 618671184832
        # 114477776340091

        device_id = int(input("enter a gateway or node id:\n"))
        
    else:
        # if mode selected involves a gateway receiving cloud messages to a gateway, then get the gateway id and reset
        # the mqtt topics.
        if gw_id == None or sink == None:
            print("{} computing gw and sink ids...".format(prefix))
            [sink, gw_id] = gvar.get_sink_and_gw(wni)
        device_id = gw_id
        
    [TOPICS_LIST, MODE_LIST] = set_mqtt_topics(device_id)
    # chose final mode and display it
    mode = MODE_LIST[mode]
    print("{} mode selected: {}, device id: {}".format(prefix, mode, device_id))
    # main script -> publish/subscribe details:
    #device_id = 2
    # [TOPICS_LIST, MODE_LIST] = set_mqtt_topics(str(device_id))

    if mode==GATEWAY_RECEIVE_CLOUD_REQUESTS_TO_NODE_MODE:
        subtopic = CLOUD_REQUEST_TO_NODE_MQTT_TOPIC
        pubtopic = GATEWAY_RESPONSE_TO_CLOUD_REQUEST_TO_NODE_MQTT_TOPIC
        inter = mqtt_interaction_cloud( subtopic, pubtopic, mode="listen", wni = wni)        
        inter.listen()

    elif mode==GATEWAY_RECEIVE_CLOUD_REQUESTS_TO_GATEWAY_MODE :
        subtopic = gvar.CLOUD_REQUEST_TO_GATEWAY_MQTT_SUPERTOPIC + str(device_id)
        pubtopic = gvar.GATEWAY_RESPONSE_TO_CLOUD_REQUEST_TO_GATEWAY_MQTT_SUPERTOPIC + str(device_id)
        inter = mqtt_interaction_cloud( subtopic, pubtopic, mode="listen", wni = wni, gw_id = gw_id, sink = sink)        
        inter.listen()
        
    elif mode==GATEWAY_SEND_CLOUD_REQUESTS_MODE:
        subtopic = CLOUD_RESPONSE_TO_GATEWAY_REQUEST_MQTT_TOPIC
        pubtopic = GATEWAY_REQUEST_TO_CLOUD_MQTT_TOPIC    
        inter = mqtt_interaction_cloud( subtopic, pubtopic, mode="request", wni = wni)        
        inter.send_message()

    elif mode==fake_cloud_node_pub:
        subtopic = GATEWAY_RESPONSE_TO_CLOUD_REQUEST_TO_NODE_MQTT_TOPIC
        pubtopic = CLOUD_REQUEST_TO_NODE_MQTT_TOPIC
        inter = mqtt_interaction_cloud(subtopic, pubtopic, mode="request", need_local_wni=False, gw_id=device_id, sink="sink0")    
        inter.send_message()

    elif mode == fake_cloud_gw_pub:
        subtopic = GATEWAY_RESPONSE_TO_CLOUD_REQUEST_TO_GATEWAY_MQTT_TOPIC
        pubtopic = CLOUD_REQUEST_TO_GATEWAY_MQTT_TOPIC
        inter = mqtt_interaction_cloud(subtopic, pubtopic, mode="request", need_local_wni=False, gw_id=device_id, sink="sink0")
        inter.send_message()

    elif mode == fake_cloud_sub:
        subtopic = GATEWAY_REQUEST_TO_CLOUD_MQTT_TOPIC
        pubtopic = CLOUD_RESPONSE_TO_GATEWAY_REQUEST_MQTT_TOPIC
        inter = mqtt_interaction_cloud(subtopic, pubtopic, mode="listen")
        inter.listen()     

    else:
        print("Unrecognized mode selected, bye")


def main():
    run_cloud_comunications()

if __name__ == "__main__":     
    main()





