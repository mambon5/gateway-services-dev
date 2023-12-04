"""
This is the basic structure for the node and cloud communications.

"""
import global_vars as gvar              #: import global variables
import time                             # to get message reception time
from struct import *                    # for pack/unpack functions
from threading import Thread
import mqtt_credentials as creds        # global and local credentials containing all the details on the MQTT broker connection (passwords, hosts, ports, etc)


class mqtt_interaction:
    """ 
    Basic interaction class. 
    The classes :py:class:`~mqtt_interaction_cloud.mqtt_interaction_cloud` and 
    :py:class:`~mqtt_interaction_node_basic.mqtt_interaction_node_basic` are extensions of this one.

    The structure of this class is the following:

    :structure:
        1. It creates the WNI if needed, and not already created.
        2. If the interlocutor is the "cloud", then it subscribe and sets a publisher to the right global MQTT topics.
        3. Finally, it has the following methods:
            - :py:meth:`~mqtt_interaction_module.mqtt_interaction.listen`
            - :py:meth:`~mqtt_interaction_module.mqtt_interaction.on_message` 
            - :py:meth:`~mqtt_interaction_module.mqtt_interaction.send_message`
            - :py:meth:`~mqtt_interaction_module.mqtt_interaction.start_listen_thread`
            - :py:meth:`~mqtt_interaction_module.mqtt_interaction.check_for_response`  
            - :py:meth:`~mqtt_interaction_module.mqtt_interaction.on_disconnect`
            - :py:meth:`~mqtt_interaction_module.mqtt_interaction.on_publish` 
            - :py:meth:`~mqtt_interaction_module.mqtt_interaction.update_with_new_message`
            - :py:meth:`~mqtt_interaction_module.mqtt_interaction.update_msg_id`  
            - :py:meth:`~mqtt_interaction_module.mqtt_interaction.set_node_id`
            - :py:meth:`~mqtt_interaction_module.mqtt_interaction.stop_sub_loop` 
            - :py:meth:`~mqtt_interaction_module.mqtt_interaction.print_sub_loop`
            - :py:meth:`~mqtt_interaction_module.mqtt_interaction.start_listen_loop`  
            - :py:meth:`~mqtt_interaction_module.mqtt_interaction.send_msg_from_input` 
            - :py:meth:`~mqtt_interaction_module.mqtt_interaction.is_a_msg_request` 
            - :py:meth:`~mqtt_interaction_module.mqtt_interaction.convert_dst_address`  
     
    :param subtopic: MQTT topic to which the client will subscribe to
    :type subtopic: string
    :param pubtopic: MQTT topic to which the client will publish to
    :type pubtopic: string
    :param mode: mode of the interaction. Can be either "listen" to receive messages from the subtopic, or "request" if we want to the entity to publish requests to the pubtopic
    :type mode: string
    :param file_settings: file containing the shared message id to update
    :type file_settings: file
    :param interlocutor: entity which we wish to communicate to. Defaults to *cloud*
    :type interlocutor: string

    :return:

        Returns a **mqtt_interaction** class with the following attributes:

            :pubclient: (mqtt.Client) -- MQTT client for publishing messages (only if interlocutor is "cloud") 
            :subclient: (mqtt.Client) -- MQTT client for subscribing to a topic (only if interlocutor is "cloud") 
            :pub_msg_id: (int) -- unique message temporal identifier for the published messages
            :gw_id: (int) -- gateway id for the interaction
            :run_loop: (bool) -- run the subclient loop, while true
            :pub_resp_received: (bool) -- whether a response for the sent message has been received
            :max_wait: (int) -- max waiting time for response before deciding no response has been received, in seconds
            :startime: (int) -- start time (in seconds) of the loop in the subclient
            :thread: (thread) -- thread to use for starting a subscriber or publisher client when needed while the main thread still runs
            :print_raw_data: (bool) -- whether or not we wish to print the raw data we get from the node
            :send_attempts: (int) -- number of times the message will be tried to be sent, if the previous attempts fail to get a matching response
            :start_countdown: *(bool)* -- Bool that detects when the listening loop timer, has to start counting down
            :msg_to_send: *(bytes)* -- Message to send to node? or cloud? probably stores the message from a tunnel connexion.
            :start_countdown: *(bool)* -- If true, it prints the left time in the wait loop countdown at every iteration
            :local_broker: *(ip)* -- ip of the local MQTT broker
            :local_port: *(int)* -- direction of the local MQTT broker port to access
            :local_user: *(string)* -- username needed to access the local MQTT broker
            :local_password: *(string)* -- password needed to access the local MQTT broker
            :local_insecure: *(bool)* -- allow insecure connection to the local MQTT broker?
            :global_broker: *(ip)* -- ip of the global MQTT broker
            :global_port: *(int)* -- direction of the global MQTT broker port to access
            :global_user: *(string)* -- username needed to access the global MQTT broker
            :global_password: *(string)* -- password needed to access the global MQTT broker
            :wni: *(WirepasNetworkInterface)* -- a wirepas network interface class connected to the selected local mqtt broker
            :need_local_wni: *(bool)* -- Whether even though wni=*None* we still need to create a wni, or not.
            
     """

    def __init__(self, subtopic=None, pubtopic=None, 
    mode="request", file_settings=gvar.FILE_SETTINGS_GLOBAL, interlocutor="cloud", wni=None, need_local_wni=True):
        """
        Initialize class interaction attributes.    
        """
        prefix = "<init basic mqtt interac> "
        
        self.subtopic = subtopic
        self.pubtopic = pubtopic
        self.mode = mode
        self.pubclient = None
        self.subclient = None
        self.pub_msg_id = None
        self.pub_resp_received = False
        self.gw_id = None
        self.sink = None
        self.run_loop = True            # run the subclient loop, while true
        self.max_wait = 2              # default max waiting time for response before deciding no response has been received, in seconds
        self.startime = None            # start time (in seconds) of the loop in the subclient
        self.thread = None
        self.interlocutor = interlocutor
        self.print_raw_data = False
        self.send_attempts = 1
        self.send_attempts_left = self.send_attempts
        self.msg_to_send = None
        self.start_countdown = False
        self.wni = wni
        self.need_local_wni = need_local_wni
        self.file_settings = file_settings        # file for storing message id and updating it:s
        

        # mqtt connection parameters:
        # global broker:
        self.broker = creds.global_broker
        self.port = creds.global_port
        try:
            self.user = creds.global_user 
            self.password = creds.global_password
        except:
            self.user = None
            self.password = None

        # local broker:
        self.local_broker = creds.local_broker
        self.local_port = creds.local_port

       
                                  
        if self.wni != None:
            print(prefix + "WirepasNetworkInterface class already created, skipping creation of a new wni.")
        elif need_local_wni:
            self.wni = gvar.create_wni()
            print(prefix + "wni class needed, we just created a new one.")
        else:
            print(prefix + "wni not needed and not created.")

        print(prefix + "initializing basic mqtt interaction class..")

        # use sink to compute gw and sink id, except if it is a fake cloud simulator.
        if gvar.get_supertopic(self.pubtopic) not in gvar.FAKE_CLOUD_PUB_SUPERTOPIC_LIST:
            if self.gw_id == None or self.sink == None:
                print("{} gw and sink are None, thus getting gw id and sink id".format(prefix))
                [self.sink, self.gw_id] = gvar.get_sink_and_gw(self.wni) # set sink and gateway id
            else:
                print("{} gateway and sink already set.".format(prefix))
            print("{} gateway id: {}, sink: {}".format(prefix, self.gw_id, self.sink))

        # since senders to the gateway, don't necessarily know what is the gateway and sink addresses.
        print(prefix + "sink and gateway set")

        print("inter class initialized")
        # if interlocutor=="cloud":
        #     print("interlocutor is a cloud")
        #     self.set_node_id()

        #     if mode=="request":
        #         # subscribe to expected response topic:    
        #         self.subclient = self.set_sub_client("(response) "+str(subtopic) +"--> subscriber")          

        #         # publish message:
        #         self.pubclient = self.set_pub_client("publisher-->"+ str(pubtopic) )

        #     elif mode=="listen":
        #         self.subclient = self.set_sub_client(""+str(pubtopic) +"--> subscriber")
        #     else:
        #         print("init mqtt_interaction() error: 'mode' not recognized")


    def listen(self):
        """
       When any interaction is set to "listen" to its interlocutor, this function is immediately called.

       :does:
            - depending on the interlocutor (cloud or nodes) it will call
                - :py:meth:`~mqtt_interaction_cloud.mqtt_interaction_cloud.listen_to_cloud`
                or

                - :py:meth:`~mqtt_interaction_node_basic.mqtt_interaction_node_basic.listen_to_nodes`
              and start the specific listening function.
        
        
        """
        prefix ="<listen> "

        if self.interlocutor == "cloud":
            self.listen_to_cloud(prefix)
        elif self.interlocutor =="nodes":
            self.listen_to_nodes(prefix)


    def on_message(self, client=None, userdata=None, data=None, sent_msg_id=None):     # cloud on message function, create function for callback
        """
        When a message is received, this callback function is invoked.
         
        :does:
            - depending on the interlocutor (cloud or nodes) it will call
                - :py:meth:`~mqtt_interaction_cloud.mqtt_interaction_cloud.on_message_c`

                or

                - :py:meth:`~mqtt_interaction_node_basic.mqtt_interaction_node_basic.on_message_nodes`
              and call the right function for processing the received message.
        
        
        :param data: message payload
        :type data: bytes

        """
        timestamp = gvar.get_timestamp()      

        prefix = "<on message> "
        print(prefix + "received at " + timestamp)
    

        if self.interlocutor == "cloud":
            self.on_message_c(client, userdata, data, sent_msg_id)
        elif self.interlocutor =="nodes":
            data = client   # in the node messages (using wirepass), the data is passed in the first argument of "on_message" function
            print(prefix + "received data: " + str(data))
            self.on_message_nodes(data)
        else:
            print(prefix + "error, message received but invalid interlocutor: " + self.interlocutor)

    def check_for_response(self, msg):
        """Checks whether the message received corresponds to any previous request.

        :does:
            1. Checks weather the response msg id matches the request msg id.
            2. If the above is true, and either the node ids or the gw ids of the received and sent messages coincide, then
               the received message is considered a received response to a previous request.
            3. If that is the case, the algorithm marks it as a received response, and stops the listening thread by calling the 
               :py:meth:`~mqtt_interaction_module.mqtt_interaction.stop_sub_loop` function.
            4. If the received message is not a response, then that is reported in the logs/console print.

        :param msg: message class
        :type msg: RxMsg

        :returns:
            :True: -- if response id matches the initial request
            :False: -- Otherwise
        """

        prefix = "<check for response>: "
        option1 = self.node_id != None and msg.id == self.pub_msg_id and msg.node_id == self.node_id
        option2 = self.gw_id != None and msg.id == self.pub_msg_id and str(msg.gw_id) == str(self.gw_id)
        print(prefix + "checking for response... msg id:" + str(msg.id) + ", iter msg id:"+str(self.pub_msg_id) + 
        ", msg.node_id:"+str(msg.node_id) + ", interaction node_id:"+str(self.node_id) + ", msg_gw_id:"+str(msg.gw_id) +", iter gw_id:"+
        str(self.gw_id))
        if  option1 or option2:
            print(prefix + "response found corresponding to request message")
            self.pub_resp_received = True                          
            self.stop_sub_loop()  
            return True
        else :
            print(prefix + "not a matching response.")

        # depending on the message type, we should also check for: 
            # CRC, num of nodes, etc...


        return False

    
    def on_disconnect(client, userdata,rc=0):
        """
        what to do if a MQTT client gets disconnected.

        :does:
            1. stops the subscribe loop by calling the function *stop_sub_loop()*

        """
        print("DisConnected result code "+str(rc))
        client.stop_sub_loop()

    def on_publish(self,client,payload):
        """
        When a message is published to either the global or local MQTT broker, this function is invoked.

        :param client: publisher client
        :type client: mqtt.Client
        :param payload: message payload
        :type payload: bytes

        """
        timestamp = gvar.get_timestamp()
        prefix = "<on publish> "
        print(prefix + "message published successfully at "+ timestamp)

        if self.interlocutor == "cloud" :
            print(prefix + "for cloud called!")
        elif self.interlocutor == "nodes" :
            print(prefix + "for nodes called!")

    # publish topic function

    def publish(self,   payload,  
                        gw_id = None,
                        sink_id = None,
                        node_id= None,
                        client=None):
        
        """
        Publishes a message to the MQTT topic.
        
        :does: 
            1. Starts a listening thread to anticipate the possible response. 
               It calls the function :py:meth:`~mqtt_interaction_module.mqtt_interaction.start_listen_thread`.
            2. It calls the publishing function, which can either be:

                - :py:meth:`~mqtt_interaction_cloud.mqtt_interaction_cloud.publish_c` if we are publishing the message to the cloud

                or

                - :py:meth:`~mqtt_interaction_node_basic.mqtt_interaction_node_basic.publish_meshnet` if we are publishing the message to the nodes.
            3. Checks if the message has been published successfully or not, and reports a message accordingly to the logs.
            4. Starts the timeout countdown for receiving a response to the just published request message. This is done by setting boolean 
               :py:data:`~mqtt_interaction_node_basic.mqtt_interaction_node_basic.start_countdown` to True.
                
        :param client: publisher client
        :type client: mqtt.Client
        :param payload: message payload
        :type payload: bytes
        :param node id: node id to who we wish to communicate
        :type node id: int
        :param gw_id: gateway id to send the message from (in case of fake cloud, *to*)
        :type gw_id: int
        :param sink_id: Sink id where nodes connect to the gateway
        :type sink_id: string   
        
        :return:
            - published (bool) -- True if publish successful, False if failed.
        """

        prefix="<inter.publish>: "
        timestamp = gvar.get_timestamp()
        published = False
        self.msg_to_send = [payload, gw_id, sink_id, node_id, client]

        if self.mode == "request": 
            #listen to incoming messages in a new thread, right before publishing the message, for request mode
            print(prefix + "start listen thread, mode:" + self.mode)
            self.start_listen_thread()

        if self.interlocutor == "cloud":
            published = self.publish_c(client,payload,prefix)
        elif self.interlocutor == "nodes":
            published = self.publish_meshnet(gw_id, sink_id, payload, node_id, prefix)
            print(prefix + "interlocutor: " + self.interlocutor)
        
        if published: 
            print(prefix+"message sent: " + str(payload) + " at: " + timestamp)
        else:
            print(prefix + "message publication failed, stoping listening thread")
            self.stop_sub_loop()

        if self.mode == "request":
            # Start the timer loop and wait for message(s) once everything is published properly and the listening also started
            print(prefix + "start timer loop, mode:" + self.mode)
            self.start_countdown = True

        return published
        
    def update_with_new_msg(self, msg):
        """
        Sets the interaction value of the *sub_msg_id* parameter, to equal that of the received message.
        """
        self.sub_msg_id = msg.id

    def update_msg_id(self):
        """
        Updates the message id that is stored in the external settings file.

        :does:
            1. Increments the value of the global message id saved in the file

                - :py:meth:`~global_settings` if we wish to publish to the cloud

                or

                - :py:meth:`~local_settings` if we wish to publish to the nodes.                
        
               by calling the function :py:meth:`~global_vars.update_msg_id`.
            2. Gets this value and saves it in the interaction parameter :py:data:`~mqtt_interaction_module.mqtt_interaction.pub_msg_id`.
        """
        self.pub_msg_id = gvar.update_msg_id(self.file_settings)

    def set_node_id(self) :
        """
        Gets the node id for messages sent to/from cloud only.

        It does so by calling the function :py:data:`~mqtt_interaction_cloud.mqtt_interaction_cloud.set_node_id_c`
        
        """
        
        if self.interlocutor == "cloud" :
            self.set_node_id_c()
        elif self.interlocutor == "nodes":
            pass
        else:
            print("<set node id> error, wrong interlocutor being used!")
            return
        

    def stop_sub_loop(self) :
        """
        Stops the listening loop that actually keeps printing the remaning time before timeout, when a message is sent
        to either the cloud or the nodes. 

        :does:
            1. sets the variable *run_loop" to False
            2. If the interlocutor is *cloud* it calls the paho mqtt function *loop_stop()* to stop the subscription to the global MQTT broker.
        """
        self.run_loop = False
        if self.interlocutor == "cloud" :
            self.subclient.loop_stop()
        self.start_countdown = False
        # self.subclient.disconnect() # disconnect the listener
        
    def print_sub_loop(self,dt,wait) :
        """
        Prints the seconds left before timeout when waiting for a response.

        :param dt: time interval from when the subscribe loop started, up to now.
        :type dt: int
        :param wait: time (in milliseconds) when the last counter was printed
        :type wait: int

        :does:
            1. Prints the seconds left before reaching *max_wait* time.
            2. At every print, it updates the time the counter was last printed in *wait*
        """

        if wait == self.startime:
            print( str(self.max_wait) + " s")
            wait = time.time()
        # print timer functions:
        dt2 = time.time()-wait
        if dt2 > 1 :
            wait = time.time()
            print( str(round(self.max_wait -dt)) + " s")
        return wait

    

    def start_listen_loop(self):      
        """Creates and starts the loop that prints the timeout time left before aborting the connection to either the cloud or the nodes.

        :does:
            If interaction mode == "listen"
                1. It does nothing, either the cloud or the node class is responsible for properly listening to all the incoming messages.
            If mode == "request"
                1. Creates a loop that lasts for *max_wait* time at most. This is a parameter of the RxMsg class.
                2. Once a matching response to the previous request, or the *max_wait* time is reached, the loop stops.
        """

        prefix = "<start timer loop> "
        # loop startime:
        self.startime = time.time()
        print(prefix+"start loop")

        # timer:
        dt = (time.time()-self.startime)
        wait = self.startime

        # main timer loop:
        # while self.run_loop and  (dt < self.max_wait or self.mode == "listen"):  
        if self.mode == "request":              
            while self.run_loop and  (dt < self.max_wait):                
                
                if self.mode == "request" and self.start_countdown:                                       
                    # update timer:                                                
                    dt = (time.time()-self.startime)                              
                    # print timer:
                    # print("dt: " + str(dt))
                    wait = self.print_sub_loop(dt, wait)  

                    time.sleep(0.02) # in order to decrease CPU usage                          
            
       
            if self.pub_resp_received:
                timestamp = gvar.get_timestamp()
                print("great! response received at " + timestamp)
            else :
                self.send_attempts_left = self.send_attempts_left - 1
                if self.send_attempts_left > 0:
                    print(prefix + "retrying to publish the message, attemps left: " + str(self.send_attempts_left))
                    list = self.msg_to_send
                    self.publish(list[0],list[1],list[2],list[3],list[4]) # this part is not very well, explained, basically we republish the same message
                elif dt >= self.max_wait:
                    print(prefix + "sheit, no answer after " + str(self.max_wait)+" seconds :/ and "+str(self.send_attempts) + " send attemps.")
                else:
                    print(prefix + "finished")
    
    def start_listen_thread(self):
        """
        
        Starts the function :py:meth:`~mqtt_interaction_module.mqtt_interaction.listen` in a new thread.
        
        
        """

        self.thread = Thread(target=self.listen)
        # self.thread.daemon = True
        self.thread.start()
        print("new thread running on background")

    def send_msg_from_input(self):
        """
        
        Sends a message based on the user input.
        
        :does:
            - depending on the interlocutor (cloud or nodes) it will call
                - :py:meth:`~mqtt_interaction_cloud.mqtt_interaction_cloud.send_cloud_msg_from_input`
                - :py:meth:`~mqtt_interaction_node_basic.mqtt_interaction_node_basic.send_msg_to_nodes_from_input`
              and call the right function for sending a new message to the desired interlocutor.

        """
        prefix = "<send msg from input> "
        if self.interlocutor == "cloud":
            self.send_cloud_msg_from_input(prefix)
        elif self.interlocutor == "nodes":
            self.send_msg_to_nodes_from_input(prefix)

    def send_message(self,gw_id = None, sink= None, node_id= None, msg_type= None, args = []):
        """Sends a message to the right interlocutor.

        :does:
            1. Calls the main :py:meth:`~mqtt_interaction_module.mqtt_interaction.send_msg_from_input` function
        """    
        if self.interlocutor == "cloud" :                
            self.send_msg_from_input()
        if self.interlocutor == "nodes":
            self.send_msg_from_input()

    def is_a_msg_request(self, msg_type):
        """
        Checks whether the message received is a message request or a message response.

        :does:
            - Returns *True* is the message received is a message request.
            - Returns *False* otherwise.
        
        """

        if self.interlocutor == "cloud":
            if msg_type in gvar.MSG_CLOUD_TO_NODE_REQUESTS_LIST or msg_type in gvar.MSG_CLOUD_TO_GATEWAY_REQUESTS_LIST or msg_type == gvar.MSG_TYPE_ERROR:
                # I added the message type error in this.
                return True
        if self.interlocutor == "nodes":
            if msg_type in gvar.MSG_NODE_REQUESTS_LIST:
                return True
    
        return False

def convert_dst_address(dst_addr):
            """
            Function to check and convert destination address parameter.
            
            :param dst_addr: node id who we wish to communicate to
            :type dst_addr: int
            
            :returns:
                :dst_addr: (int) -- destination address converted from decimal or hexadecimal format to integer
                :res: (bool) -- conversion status (True: conversion successful, False: conversion failed)
            """
            res = False

            # try to convert parameter from decimal or hexadecimal format to integer
            try:
                dst_addr = int(dst_addr)
                res = True
            except ValueError:
                try:
                    dst_addr = int(dst_addr, 16)
                    res = True
                except ValueError:
                    print("Wrong parameter value given ! <destination address> must be an integer (decimal or hexadecimal format)")

            return dst_addr, res


