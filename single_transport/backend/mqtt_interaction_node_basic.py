"""

Basic node to gateway interaction class

"""

from message_received_class import RxMsg
import mqtt_interaction_module as interm
from mqtt_interaction_module import mqtt_interaction
import sys
import global_vars as gvar              #: import global variables
import mqtt_credentials as creds        # global and local credentials containing all the details on the MQTT broker connection (passwords, hosts, ports, etc)
import create_message_functions as creamsgf     #create message functions


try:
    import wirepas_mesh_messaging as wmm
except ModuleNotFoundError:
    print("Please install Wirepas mesh messaging wheel: pip install wirepas-mesh-messaging")
    sys.exit(-1)

class mqtt_interaction_node_basic(mqtt_interaction):
    """
    Basic mesh network mqtt interaction class. 
    
    The classes :py:meth:`~mqtt_interaction_node_main.mqtt_interaction_node_main` and 
    :py:meth:`~mqtt_interaction_node_temporal.mqtt_interaction_node_temporal` are extensions of this one.

    The structure of this class is the following:

    :structure:
        1. It initializes the sub class :py:meth:`~mqtt_interaction_module.mqtt_interaction` and gives the following parameters to it:
            - subtopic
            - pubtopic
            - mode
            - local file for message id upadtes
            - interlocutor 
            - WNI (can be None)
        2. Sets the timout time for listening to a response message, to 7 seconds.
        3. Finally, it has the following methods:
            - :py:meth:`~mqtt_interaction_node_basic.mqtt_interaction_node_basic.on_message_nodes`
            - :py:meth:`~mqtt_interaction_node_basic.mqtt_interaction_node_basic.publish_meshnet`
            - :py:meth:`~mqtt_interaction_node_basic.mqtt_interaction_node_basic.listen_to_nodes` 
            - :py:meth:`~mqtt_interaction_node_basic.mqtt_interaction_node_basic.send_message_to_nodes_from_input`  
            - :py:meth:`~mqtt_interaction_node_basic.mqtt_interaction_node_basic.request_to_node`
            - :py:meth:`~mqtt_interaction_node_basic.mqtt_interaction_node_basic.on_gateway_answer_callback` 
            
    
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

        Returns a **mqtt_interaction_node_basic** class with the following attributes:

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
            :tunnel: (cloud_to_node_tunnel) -- class for establishing a connection between a cloud interaction and a node interaction
            :node_response: (RxMsg) -- The message containing the received response from the nodes
            :wni: *(WirepasNetworkInterface)* -- a wirepas network interface class connected to the selected local mqtt broker     """

    def __init__(self, mode, wni=None):

        prefix = "<init mqtt node interac> "
        subtopic = None
        pubtopic = None
        interlocutor = "nodes"
        self.node_response = None
        # Connect to MQTT broker.
        # print(prefix + "connecting to {}:{} ...".format(creds.local_broker, creds.local_port))
        
        mqtt_interaction.__init__(self, subtopic, pubtopic, mode, 
                                         gvar.FILE_SETTINGS_LOCAL,  interlocutor, wni=wni)       

        self.max_wait = 7         # default max waiting time for response before deciding no response has been received, in seconds

        prefix = "<mqtt_interaction_node_basic innit>: "

    def publish_meshnet(self, gateway_id, sink_id, payload, node_id, prefix=""):
            """
            Publishes a message to the mesh network. 
            
            :does:
                1. Tries to send the message to the mesh network using the *wirepas_interaction_network* function :py:meth:`~wirepas_network_interface.send_message`.
                   For that to work, it has to give the following variables to the wirepas function:
                        - *gateway_id* -- that will transmit the message
                        - *sink_id* -- that will send the message to the right node
                        - *node_id* -- of the target node
                        - *src_ep*
                        - *dst_ep*
                        - *payload* -- of the message 
                        - *Quality of Service* (QOS) -- of the desired MQTT connection
                        - *callback* -- function in case an error is reported
                2. Report in the logs if the publish was successful or not.
                   

            :note: It is the mesh-network equivalent to the 
                   :py:meth:`~mqtt_interaction_cloud.mqtt_interaction_cloud.publish_c` cloud interaction function.

            :param payload: message payload, has a variable length
            :type payload: bytes
            :param gateway_id: gateway id to who the message was sent.
            :type gateway_id: int
            :param sink_id: sink id that received the message in the gateway
            :type sink_id: int
            :param node_id: node id where we want to send the message.
            :type node_id: int
            :param prefix: parent prefix to append to the current prefix. This will be reported in all prints made by this function
            :type prefix: string

    
            :returns:
                - **True** if message was sent successfully, an error if not.
            """
            prefix = prefix + "node msg publish> "

            src_ep = gvar.UPLINK_PACKET_EVAL_APP_ENDPOINT
            dst_ep = gvar.UPLINK_PACKET_EVAL_APP_ENDPOINT
            qos = 1
            
            res = False
            try:
                # send message:
                res = self.wni.send_message(gateway_id,
                                            sink_id,
                                            node_id,
                                            src_ep,
                                            dst_ep,
                                            payload,
                                            qos,
                                            cb=self.on_gateway_answer_callback)
            
            except Exception as e:
                print(prefix + "error in sending msg: " + str(e))

            if res == None: 
                res = True # successful return from send_message
                print(prefix + "message sent successfully")
            else:
                print(prefix + "message failed to send.")
            return res

    def listen_to_nodes(self, prefix):
        """
            Listens to node messages. 

            :does:
                1. Sets a wirepass filter
                2. Sets a callback on any received data from the nodes, in our cass the cb is :py:meth:`~mqtt_interaction_module.mqtt_interaction.on_message`
                3. If the mode is "request", it will: 
                    - start the :py:meth:`~mqtt_interaction_module.mqtt_interaction.start_listen_loop` loop, to continuously listen to wirepass messages
                    - Once the loop finishes (for whatever reason) it removes the wirepas filter for the callback
                   If the mode is "listen" it doesn't do anything else.
            
            :note: This is the equivalent function to the :py:meth:`~mqtt_interaction_cloud.mqtt_interaction_cloud.listen_to_cloud` 
                   function in the interaction cloud class.

            :param prefix: parent prefix to append to the current prefix. This will be reported in all prints made by this function
            :type prefix: string

            :returns:
                - **True** if successful, an error if not.
        """
        # console logs:
        prefix = prefix + "nodes> "
        print(prefix + "started listening")

        # Register for incoming data and store reception filter ID
        filter_id = self.wni.register_data_cb(self.on_message,
                                              src_ep=gvar.UPLINK_PACKET_EVAL_APP_ENDPOINT,
                                              dst_ep=gvar.UPLINK_PACKET_EVAL_APP_ENDPOINT
                                              )
        if self.mode == "request":
            # Start loop and wait for message(s)
            self.start_listen_loop()

            # Unregister from data reception and return to main shell menu.
            self.wni.unregister_data_cb(filter_id)

    def send_msg_to_nodes_from_input(self,prefix=""):
        """
        Prepares and sends a message to the nodes, based on the user input.

        :does:
        
            1. Update the message id, takes the last one from the *local_settings.py* file, and increments it by 1 by calling the function
               :py:meth:`~mqtt_interaction_module.mqtt_interaction.update_msg_id`.
            2. Generates the initial message payload in bytes, by calling the function
               :py:meth:`~create_message_functions.get_msg_from_input`.
            3. It finally calls the :class:`request_to_node <mqtt_interaction_node_basic.request_to_node>` function and provides it the following
               parameters:
                - *gw_id* -- gateway id
                - *sink_id* -- sink id
                - *dst_addr* -- id of the node we want to send the message to
                - *payload* -- initial payload of the message in bytes, which so far just contains the message id and type.
        
        :note:  This is the mesh network equivalent function to the 
                    :py:meth:`~mqtt_interaction_cloud.mqtt_interaction_cloud.send_cloud_msg_from_input` function in the cloud class.

        """
        prefix = prefix + "to nodes> "
        
        self.update_msg_id()
        payload = creamsgf.get_msg_from_input(self.pub_msg_id, self.pubtopic)
        self.request_to_node(gw_id = gvar.gw_id, sink_id = gvar.sink, dst_addr = gvar.node_id, payload = payload)
         
    def request_to_node(self, gw_id, sink_id, node_id, msg_type=None, args = [], payload=None):
        """
            Sends messages to the mesh network. 
            
            :does:
                1. If the payload is *None*:
                    -   It updates the message id, takes the last one from the *local_settings.py* file, and increments it by 1 by calling the function
                        :py:meth:`~mqtt_interaction_module.mqtt_interaction.update_msg_id`.
                    -   Puts all the message information to bytes using the  :py:meth:`~create_message_functions.message_to_bytes`  function
                2. Stores the information regarding the message to be sent, in a database (if applicable)
                3. Gets the current timestamp in order to know when we sent the message, using the function :py:meth:`~global_vars.get_timestamp`
                4. Sends the message by running the :py:meth:`~mqtt_interaction_module.mqtt_interaction.publish` function.
                5. Prints whether the message was sent or there was an error.

            :note:  This function can be called in 2 ways: 
                        1. providing the payload
                        2. providing msg_type and arguments
                    In both cases you have to provide the gateway id, sink id, and node id.

            :param gw_id: gateway id to who the message was sent.
            :type gw_id: int
            :param sink_id: sink id that received the message in the gateway
            :type sink_id: int
            :param node_id: node id where we want to send the message.
            :type node_id: int
            :param msg_type: Type of message that we want to send
            :type msg_type: int
            :param args: Additional message arguments, depending on the message type
            :type args: list

            :return:
                Nothing, so far

           
        """
        prefix="<send node msg>: "
        # in order to broadcast to everyone: send_set_led_on_command 141009632514693 sink0 0xFFFFFFFF
        pub_supertopic = gvar.get_supertopic(self.pubtopic)
        result = [False, None]

        # Check parameters and convert them to the right data type.
        (node_id, addr_ok) = interm.convert_dst_address(node_id)
        
        print(prefix + "converted dst-Addr: " + str(node_id))
        
        # self.node_id = str(node_id)
        self.gw_id = str(gw_id)

        if not addr_ok :
            print(prefix + "destination address must be an integer (decimal or hex format)")
            return
        
        # OVERWRITE THE previous value for msg id, and increment by 1. Also check its limit (2 bytes)
        global message_id
                    
        # generate message content if not already present
        if payload == None:
            print(prefix + "sending message using msg.args")
            if self.mode == "request": # meaning this is a request message            
                # update the external variable (in local_settings.py) message_id, to keep track of it.
                self.update_msg_id()
                message_id = self.pub_msg_id
            payload = creamsgf.message_to_bytes(message_id, msg_type, args, pub_supertopic, prefix)            

        else:
            print(prefix + "sending message from given payload")

        # timestamp for certain purposes        
        timestamp = gvar.get_timestamp()

        # Register message to table requests_sent
        save_messages = 0
        if save_messages == 1:             
            # in case we enabled message info storing, then go ahead and store info from messages into db:
            print("arguments:" + " ".join([str(elem) for elem in [message_id, msg_type, gw_id, sink_id, node_id, timestamp]]))
            
            self._register_gw_request_message(message_id, msg_type, gw_id, sink_id, node_id, timestamp)

        # preping message:
        print(prefix + "preparing the message at {} to gateway <{}>, to sink <{}>, to node <{}> with msg id: \
            {}, message type = {} and payload={}".format(timestamp, gw_id, sink_id,node_id, self.pub_msg_id, 
            msg_type,  gvar._bytes_to_str_hex_format(payload)))

        # timestamp to control the time message was sent        
        timestamp = gvar.get_timestamp()

        # send message to the wirepass network
        sent=False
        try:
            sent = self.publish(payload = payload, gw_id = gw_id,
                                        sink_id = sink_id,                                        
                                        node_id = node_id)
        except:
            print(prefix + "failed to send the message")

        print(prefix + "result from wirepas send message: {}".format(sent))


    def on_gateway_answer_callback(self, gw_error_code, param):
        """
        Callback called when gateway publishes a message to the mesh network.
        
        :does:
            1. More precisley, this callback is called when a message is received on the "gw-response/" local MQTT topic.
            2. In this script a message will be printed only if an error is raised.

        :note:    
            By construction, every message published to this MQTT topic is a response to a previous request made to the nodes.

        :param gw_error_code: error code
        :type gw_error_code: bool?
        :param param: error parameteres¿? It just displays 'None' when there is no error, so we cannot use this as the response, or yes?
        :type param: list? 

        :does:
            1. Print an error message only if an error is raised.
        """
        prefix = "<gw request callback msg>"
        
        if gw_error_code != wmm.GatewayResultCode.GW_RES_OK:
            print("Message sending failed: res=%s. Caller param is %s" % (gw_error_code, param))
        # else:
        #     print("{} msg from node received with params: {}".format(prefix, param))
        # params is empty and displays 'None'


    # this is the alternative function to the "on_listen" function defined in the main mqtt_interaction class for cloud ineractions
    def on_message_nodes(self, data):
        """
        Every time a message is received from the mesh network, this function is invoked. 
        
        :does:
            1. We get the timestamp of when the message is received
            2. We create a *RxMsg* class with all the raw info from the wirepass.data input
            3. We parse the message payload, in order to extract the *message type* and *additional arguments* (if applicable)
            4. If the parsing is successful, 
                - The message is displayed
                - If the mode == "request" then
                    - We call the function :py:meth:`~mqtt_interaction_node_temporal.mqtt_interaction_node_temporal.on_message_temporal_node`
            5.  If mode == "listen" 
                - We just call the function :py:meth:`~mqtt_interaction_node_main.mqtt_interaction_node_main.on_message_main_node_listen`

        :note:
            1.  It is the equivalent to the :py:meth:`~mqtt_interaction_cloud.mqtt_interaction_cloud.on_message_c` function of the
                mqtt_interaction_cloud class.

        :references:
            1. It is useful to check the wirepas mqtt library documentation -> https://wirepas.github.io/wirepas-mqtt-library/ 

        :param data: a list containing various different information regarding the message. It includes the raw payload, the node id, the gateway id, the sink id.
        :type data: wirepass.data

      
        """
        timestamp = gvar.get_timestamp()
        prefix = "<on_message_event (nodes)>: "
        # use this timestamp from when the mesage is received
         
        # Init and process received message payload.
        msg = RxMsg(data.data_payload, source_address=data.source_address, gw_id=data.gw_id, sink_id=data.sink_id, rawdata=data)
        print("\n"+prefix+"#############  NODE data received: ###############")
        # initial parsing:
        # msg.parse_basic(self.subtopic) # basic parse already done in parse
        
        # parse received message    
        parsed = msg.parse(self.subtopic, self.mode)

        if parsed:
            print(prefix+"parsing finished successfully") 

            msg.display(timestamp, self.print_raw_data) 

            if self.mode == "request" :
                self.on_message_temporal_node(msg, timestamp)

        else:
            print(prefix +"Parsing failed: Invalid message received (unexpected byte length or msg type?) !\n")
            # add code around here to save recieved message via callback function... Probably?

        if self.mode == "listen" :  
            
            self.on_message_main_node_listen(msg, parsed)

  
