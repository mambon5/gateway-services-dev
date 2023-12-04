"""
This file contains all the main details of the interaction between the gateway and the cloud. 

The remaining details involve the file :py:mod:`~interaction_tunnel` file and in particular the tunneling classes:
    - :py:mod:`~interaction_tunnel.node_to_cloud_tunnel`
    - :py:mod:`~interaction_tunnel.cloud_to_node_tunnel`
"""

import global_vars as gvar              #: import global variables
import create_message_functions as creamsgf # crea message functions
from mqtt_interaction_module import mqtt_interaction
from message_received_class import RxMsg
import paho.mqtt.client as mqtt         #: in order to develop mqtt clients in python
import interaction_tunnel as intunnel
import update_gw_database as updb
import read_gw_database as readdb
import update_gw_software as upsoft
import prepare_response as sdresp

class mqtt_interaction_cloud(mqtt_interaction):
    """ 
    Cloud to gateway mqtt interaction class. 
    
    :structure:

        1. It can be used for:
            - Recieving cloud messages to the gateway
            - Receiving the cloud messages aimed at a specific node
            - Sending messages from a node to the cloud
            - Sending messages from the gateway to the cloud
        2. It handles all the interaction and messages from Cloud to Gateway. Every
           create/send/parse/display/etc method on the cloud-gateway messaging, is handled by this class.
        5. Tt has the following methods:
            - :py:meth:`~mqtt_interaction_cloud.mqtt_interaction_cloud.on_connect`
            - :py:meth:`~mqtt_interaction_cloud.mqtt_interaction_cloud.on_subscribe`
            - :py:meth:`~mqtt_interaction_cloud.mqtt_interaction_cloud.on_message_c`
            - :py:meth:`~mqtt_interaction_cloud.mqtt_interaction_cloud.send_cloud_msg_from_input`
            - :py:meth:`~mqtt_interaction_cloud.mqtt_interaction_cloud.set_pub_client`
            - :py:meth:`~mqtt_interaction_cloud.mqtt_interaction_cloud.set_sub_client`
            - :py:meth:`~mqtt_interaction_cloud.mqtt_interaction_cloud.connect_pub_client`
            - :py:meth:`~mqtt_interaction_cloud.mqtt_interaction_cloud.connect_sub_client`
            - :py:meth:`~mqtt_interaction_cloud.mqtt_interaction_cloud.publish_c`
            - :py:meth:`~mqtt_interaction_cloud.mqtt_interaction_cloud.set_node_id_c`
            - :py:meth:`~mqtt_interaction_cloud.mqtt_interaction_cloud.listen_to_cloud`          

    
    
    :param subtopic: MQTT topic to which the client will subscribe to
    :type subtopic: string
    :param pubtopic: MQTT topic to which the client will publish to
    :type pubtopic: string
    :param mode: mode of the interaction. Can be either "listen" to receive messages from the subtopic, or "request" if we want to the entity to publish requests to the pubtopic
    :type mode: string
    :param file_settings: file containing the shared message id to update
    :type file_settings: file
    :param interlocutor: interaction mode interlocutor, or entity the gateway communicates to, it can be either "cloud" or "nodes".
    :type interlocutor: string

    :return:

        Returns a **mqtt_interaction_cloud** class with the following attributes:

            :pubtopic: (string) -- MQTT publication topic of the gateway to the cloud
            :subtopic: (string) -- MQTT subscription topic to which the gw subscribes to in the global MQTT
            :pubclient: (mqtt.Client) -- MQTT client for publishing messages (only if interlocutor is "cloud") 
            :subclient: (mqtt.Client) -- MQTT client for subscribing to a topic (only if interlocutor is "cloud") 
            :pub_msg_id: (int) -- unique message temporal identifier for the published messages
            :node_id: (int) -- node id concerning the interaction
            :run_loop: (bool) -- run the subclient loop, while true
            :pub_resp_received: (bool) -- whether a response for the sent message has been received
            :max_wait: (int) -- max waiting time for response before deciding no response has been received, in seconds
            :startime: (int) -- start time (in seconds) of the loop in the subclient
            :thread: (thread) -- thread to use for starting a subscriber or publisher client when needed while the main thread still runs
            :print_raw_data: (bool) -- whether or not we wish to print the raw data we get from the node
            :tunnel: (cloud_to_node_tunnel) -- class for establishing a connection between a cloud interaction and a node interaction
            
     """
    # modes: 1-request "request" 2-listen "listen"
    # if mode is request, then first publishes to pubtopic, then awaits for 
    # response in subtopic
    # if mode is "listen" then listen to a message at subtopic, then respond to it at pubtopic

    # init the class
    def __init__(self,  subtopic, pubtopic, mode="request", wni=None, need_local_wni = True, gw_id = None, sink = None):
        """
        Initialize mqtt interaction cloud class 
        """
        prefix="<mqtt cloud interac init>"
        interlocutor="cloud"
        file_settings = gvar.FILE_SETTINGS_GLOBAL

        mqtt_interaction.__init__(self, subtopic, pubtopic, mode, 
                                         file_settings,  interlocutor, wni=wni, need_local_wni=need_local_wni)      
    
        self.subtopic = subtopic
        self.pubtopic = pubtopic
        self.mode = mode
        self.pubclient = None
        self.subclient = None
        self.pub_msg_id = None
        self.sub_msg_id = None
        self.pub_resp_received = False
        self.node_id = None
        self.run_loop = True            # run the subclient loop, while true
        self.max_wait = 14              # max waiting time for response before deciding no response has been received, in seconds
        self.startime = None            # start time (in seconds) of the loop in the subclient
        self.thread = None
        self.interlocutor = interlocutor
        self.print_raw_data = False
        self.tunnel = None
        
        if gvar.get_supertopic(self.pubtopic) in gvar.FAKE_CLOUD_PUB_SUPERTOPIC_LIST: # if it is a fake cloud do this:
            #print("{} seting the interaction gw id and sink, gw id: {}, sink: {}".format(prefix, gw_id, sink))
            self.gw_id = gw_id
            self.sink = sink

        # file for storing message id and updating it:
        self.file_settings = file_settings
        
        
        self.set_node_id()
        if self.gw_id == None:
            [self.sink, self.gw_id] = gvar.get_sink_and_gw(self.wni)
        #     # this is for the simulated cloud
        #     # this case should be deleted or unused for production purposes, only use for development

        # if self.gw_id == None or self.sink == None:
        #         print("{} finding the gateway id and sink id using the WNI...".format(prefix))
        #         [self.sink, self.gw_id] = gvar.get_sink_and_gw(self.wni)
        # else:
        #     print("{} sink and gateway id already given to cloud listener".format(prefix))
        print("{} gateway id: {}, sink id: {}".format(prefix,self.gw_id, self.sink))

        if mode=="request":
            # subscribe to expected response topic:    
            self.subclient = self.set_sub_client("(response) "+str(subtopic) +"--> subscriber")          

            # publish message:
            self.pubclient = self.set_pub_client("publisher-->"+ str(pubtopic) )

        elif mode=="listen":
            self.subclient = self.set_sub_client(""+str(pubtopic) +"--> subscriber")
        else:
            print("init mqtt_interaction() error: 'mode' not recognized")

    # callback functions on publish/subscribe/connect:
    def on_connect_sub(self, client, userdata, flags, rc, properties=None, qos=1):
        """
        Callback function for new connection from a subscriber client. 
        
        """
        prefix = "<on subscriber connect> "
        print(prefix+ str(client._client_id) + " connected to the global MQTT broker")
        print("{} subscribing to topic: ".format(prefix)+ self.subtopic + " ...")
        client.subscribe(self.subtopic, qos)
        # client.subscribe(self.subtopic,options=mqtt.SubscribeOptions(qos=1))
        if gvar.get_supertopic(self.subtopic) == gvar.CLOUD_REQUEST_TO_GATEWAY_MQTT_SUPERTOPIC:
            ip = "0.0.0.0"
            payload = gvar.pack_into_bytes("<BBBB", [int(ip.split(".")[0]), int(ip.split(".")[1]), int(ip.split(".")[2]), int(ip.split(".")[3])] ) 
            client.publish("gw-req/gw-init/{}".format(self.gw_id), payload, 1)       # publish mssage

    def on_connect(self, client, userdata, flags, rc, properties=None, qos=1):       #create function for callback
        """
        callback function on a new connection. (when CONNACK is received from the MQTT broker basically)
        
        when it connects, it has to:
            - subscribe the listeners
            - send alive signal for the cloud-gw interaction of "listen" mode (maybe not needed since already done with the send ip thing)
             
        This way we assure that if a restart of the server happens, 
        it will always subscribe again to the right mqtt topics and not loose the control of the messaging.

        """

        prefix = "<on connect> "
        print(prefix+ str(client._client_id) + " connected to the global MQTT broker")

        # if self.mode == "listen":
        #     print("{} subscribing to topic: ".format(prefix)+ self.subtopic + " ...")
        #     client.subscribe(self.subtopic, qos)
        #     # client.subscribe(self.subtopic,options=mqtt.SubscribeOptions(qos=1))
            
            
        
        

    def on_subscribe(self, client, userdata, mid, granted_qos):       #create function for callback
        """callback function on a new subscription"""
        prefix = "<on subscribe> "
        print(prefix+ str(client._client_id) +" subscribed to global MQTT broker")
        
        

    def on_message_c(self,client,userdata,data, sent_msg_id):     # cloud on message function, create function for callback
        """
        When a cloud message is received, this callback function is invoked.
         
        :note:  This function has a lot of arguments that we don't use
                but we must keep, since the paho.mqtt library sends them anyway and we need to pick just the one that interests us. Arguments
                that we don't use: "client, userdata, sent_msg_id".

        :does:
            if **mode == "listen":**

            1. Parses the message and stores temporal information on the class :py:meth:`~message_received_class.RxMsg`
            2. Displays the rellevant information on the message: *id*, *type*, additional arguments (if applicable)
            3. Tunnels to the node network (if applicable)
            4. Updates software (if applicable)
            5. Updates database (if applicable)
            6. Read the database (if applicable)
            7. Prepares de the response using the previous results, and the function :py:meth:`~interaction_tunnel.tunnel_to_node`
             
            
            8. Opens an interaction with the nodes using the function :py:meth:`~interaction_tunnel.tunnel_to_node` (if applicable)
            9. Once the node-interaction is resolved, sends a response back to the cloud
            
            alternatively if **mode == "request"**

            1. It just parses and checks the response to the previous request.
            2. If the response is NOT Okay, the execution continues and the message is ignored as if it wasn't received.
        
        :references:
            Take a look at the documentation on the python paho.mqtt *on_message* function arguments here -> http://www.steves-internet-guide.com/receiving-messages-mqtt-python-client/

        :param data: message payload
        :type data: bytes

        """
        
        timestamp = gvar.get_timestamp()
        prefix = "<received msg>: " 
        msg = RxMsg(data.payload, data.topic, gw_id=self.gw_id, sink_id=self.sink)
        
        #parse message:
        print("\n"+prefix+"#############  CLOUD data received: ###############")

        parsed = msg.parse(self.subtopic, self.mode)

        if parsed :         # using the parsing functions already created on the class RxMsg       
            print(prefix + "parsed args")
            print(msg.args)      
            self.update_with_new_msg(msg)                # updates values of the interaction class with the parsed msg information
            
            # display message:
            msg.display(timestamp)
            
            # we are only interested in the "request" mode, if the parsing is successul, since the message received will be a response to our request already
            if self.mode == "request": # how to listen to response messages to our requests

                print(prefix +"possible response received: \n{} {}\n".format(msg.topic, msg.payload))
                self.check_for_response(msg)

        else :
            print(prefix+"message parsing failed, preping an error response")
 
        if self.mode == "listen":                   # how to listen to general messages sent to us

            # set publication client in case a response to cloud is necessary (it always is lol):
            self.pubclient = self.set_pub_client("publisher (response)-->"+self.pubtopic)

            nodetunel = intunnel.tunnel_to_node(self, msg, self.wni)
            
            # update software:
            software_update = upsoft.update_gw_software(msg, self.mode, self.interlocutor)
            
            # update database::
            update_db = updb.update_gw_database(msg, self.mode, self.interlocutor)
            
            # read database::
            read_db = readdb.read_gw_database(msg, self.mode, self.interlocutor, self)
        
            # prepare response:
            result = sdresp.prepare_response(msg, parsed, update_db, read_db, self.mode, self.interlocutor, self.pubtopic, nodetunel, software_update)
            
            # error in prep response
            if not result[0]:
                print(prefix + "response preparation failed. Quitting execution..")
                return
            
            payload = result[1]
            # send response message if recieved message is a cloud request
            if self.is_a_msg_request(msg.type):
                if self.publish(payload = payload, client = self.pubclient) :
                    print(prefix + "response sent successfully")
                else :
                    print(prefix + "error: in publishing, response not sent. Message payload: " + str(payload))
            else:
                print("{} message received not of type 'request'".format(prefix))


    def send_cloud_msg_from_input(self, prefix = ""):
        """
        Sends a message based on the user input.

        :does:
            1. Updates the message id, both in the temporary memory of this script, and in the settings file.
            2. It gets the message paylod based on the user input, via the function *get_msg_from_input*
            3. Starts a new computing thread in which a subscribing client starts to listen for possible responses
            4. Publishes the message to the MQTT broker
            5. Block the main execution, until the opened thread has found a result and finished her task.
        """

        # payload = literal_eval(input("payload: "))    
        self.update_msg_id()
        payload = creamsgf.get_msg_from_input(self.pub_msg_id, self.pubtopic)
            
        # publish message
        ret = self.publish(payload = payload, client=self.pubclient)
        

        # tell pc to wait for sub thread to finish:
        self.thread.join()

        # code here will only execute after subscribin thread has finished


    # setting pub client functions:
    # publisher: (following -> http://www.steves-internet-guide.com/publishing-messages-mqtt-client/)
    # I was following these pages to do this: https://techoverflow.net/2021/12/27/how-to-set-username-password-in-paho-mqtt/

    def set_pub_client(self, client_name):
        """Creates a cloud mqtt.Client to act for publishing messages.
        
        :param client_name: name we wish to give to the publisher. 
        :type client_name: string

        :does: 
            1. Creates the client
            2. Defines the on_publish function
            3. sets username and password (if applicable)
            4. Connects the client to the MQTT broker

        :returns:

            Returns the client

                :client: (mqtt.Client) -- MQTT client for publishing messages
        
        """
        # client_name = client_name + " " + gma() + " " + gvar.get_timestamp()
        # client= mqtt.Client(client_name) 
        # we won't give a client_id, since this must be unique and the MQTT broker won't allow repeated ones, and 
        # we might need repeated client ids if more than one gateway (by mistake or not) subscribes to the same 
        # cloud messages.
        client= mqtt.Client() 
        client.on_publish = self.on_publish
        client.on_connect    = self.on_connect
        if self.user != None: 
            client.username_pw_set(self.user, self.password)
        self.connect_pub_client(client)   # establish connection

        return client

    # Client name could consist of client_name + mac_address + current_timestamp()
    # setting sub client functions:
    # subscriber: (following -> http://www.steves-internet-guide.com/subscribing-topics-mqtt-client/)

    def set_sub_client(self, client_name):  
        """
        Creates a cloud mqtt.Client to act for receiving messages.
        
        :param client_name: name we wish to give to the publisher. 
        :type client_name: string

        :does: 
            1. Creates the client
            2. Defines the on_message_c received function
            3. Sets username and password (if applicable)
            4. Connects the client to the MQTT broker

        :returns:

            Returns the client

                :client: (mqtt.Client) -- MQTT client for receiving messages
        
        """  
        # client name must be unique or subscription/publication will fail
        # client_name = client_name + " " + gma() + " " + gvar.get_timestamp()
        # client= mqtt.Client(client_name) 
        # we won't give a client_id, since this must be unique and the MQTT broker won't allow repeated ones, and 
        # we might need repeated client ids if more than one gateway (by mistake or not) subscribes to the same 
        # cloud messages.
        client= mqtt.Client() 
        client.on_subscribe = self.on_subscribe                          #assign function to callback  
        client.on_connect    = self.on_connect_sub   
        if self.user != None: 
            client.username_pw_set(self.user, self.password)       
        client.on_message = self.on_message

        self.connect_sub_client(client)
        # sub_thread.daemon = True
            
        return client
    
    # connect sub client functions:

    def connect_sub_client(self, client, keepalive=6000, qos = 1): 
        """Connects the client to the MQTT broker
        
        :param client: subscriber client
        :type client: mqtt.Client

        :does: 
            1. If this interaction is the main gateway interaction subscribed directly to cloud messages to the gateway, then 
               it sets a last will message in order to inform the cloud this gateway lost the connection.
            2. Connects the client to the MQTT broker
            3. Subscribes the client to the subscription topic specified when creating the interaction
        
        """  
        prefix = "<connect sub client cloud>"
        print("{} host: {}, port: {}".format(prefix, str(self.broker),  str(self.port)) )     
        if gvar.get_supertopic(self.subtopic) == gvar.CLOUD_REQUEST_TO_GATEWAY_MQTT_SUPERTOPIC:
            print("{} this should be a gateway listening to the cloud".format(prefix))
            payload = gvar.pack_into_bytes("<Q",[int(self.gw_id)])
            topic = gvar.GATEWAY_LAST_WILL_MSG_MQTT_SUPERTOPIC +self.gw_id
            print("{} message as last will: {} with payload: {}".format(prefix,topic,payload ))
             
            client.will_set(topic, payload, 0, False)
        client.connect(self.broker,self.port, keepalive=keepalive)   # establish connection
        # I could use connect_async() instead
       
        # if self.pub_resp_received == False :
        #     print("no response received after 10s ... :(")
        # else:
        #     print("Correct response received!")

    # connect pub client functions:

    def connect_pub_client(self, client, keepalive=6000):        
        """Connects the client to the MQTT broker
        
        :param client: publisher client
        :type client: mqtt.Client

        :does: 
            1. Connects the client to the MQTT broker
        """ 
        
        client.connect(self.broker,self.port, keepalive=keepalive)   # establish connection
        print("publish client connected, ready to publish to topic: "+ self.pubtopic + " ...")
    
    # publish topic function
    def publish_c(self,client,payload, prefix="", qos=1):
        """Publishes a message to the MQTT topic.
 
        :does: 
            1. Publishes the message payload to the publish topic. This topic was defined when we created the interaction

        
        :param client: publisher client
        :type client: mqtt.Client
        :param payload: message payload
        :type payload: bytes
        
        :return: 
            **res** (*bool*) -- True if the publication is successful, False otherwise

        """
        prefix=prefix + "cloud> "
        timestamp = gvar.get_timestamp()
        res = False

        print(prefix+"publishing message: " + str(payload) + " sent at: " + timestamp)
        
        try:
            client.publish(self.pubtopic, payload, qos)
            print("publish successful")
            res = True
        except :
            print("publish failed")
            print("retry after 10 sec")

        return res
  
    def set_node_id_c(self) :
        """
        Gets the node id for messages sent to/from cloud"""
        
        prefix = "<set node id for cloud> "
        if self.subtopic.split("/")[1] == "n":
            self.node_id = self.subtopic.split("/")[2]
        elif self.subtopic.split("/")[1] == "gw":
            self.node_id = gvar.broadcast_address
        print(prefix + "node id set to {}".format(self.node_id))
    

    def listen_to_cloud(self, prefix=None):
        """
        Starts the listening function for incoming cloud messages to the gateway.
        
        :does:
            1. Starts the "loop_start()" mqtt paho function, which handles automatic reconnects and calls the loop method regularily in a new thread
        
        """
        prefix = "<cloud listen> "
        print(prefix + "to node id: {}".format(self.node_id))

        if self.mode=="listen":
            self.subclient.loop_forever()
        else:
            self.subclient.loop_start() # starts the mqtt loop
            self.start_listen_loop()


    
