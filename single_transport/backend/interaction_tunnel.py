"""
This file passes messages between:

1. cloud --> node 
2. node --> cloud

In order to do so, there are two classes. One that creates a tunnel from cloud --> node and another one that creates the 
tunnel from node --> cloud, respectively.

1. The *cloud --> node* tunnel, is created when the cloud sends a message to a specific node. In particular, when the gateway receives
   a cloud message targeted at a node "n", then it will create a :py:meth:`~mqtt_interaction_node_temporal.mqtt_interaction_node_temporal` class
   with mode set to "request" in order to send messages to the desired node.
2. The *node --> cloud* tunnel is created when the gateway detects a new node in its network. It is created in order to receive messages
   from the cloud to this new node. This tunnel basically creates an 
   :py:meth:`~mqtt_interaction_node_basic.mqtt_interaction_node_basic` class that "listens" to new cloud messages for that node.
"""

import mqtt_interaction_cloud
import mqtt_interaction_node_temporal
import global_vars as gvar              #: import global variables
from message_received_class import RxMsg
import otap_specific_functions as remotap
from wirepas_mqtt_library import WirepasOtapHelper

class cloud_to_node_tunnel :
    """ 
    This class is created when the gateway receives a cloud message that is pointed at a specific node. The gateway will then
    create this class in order to transmit the message to the node and make the final step in the transmission. 

    :param cloud_inter: cloud interaction of the gateway. We need to pass the whole interaction in order to allow the tunnel to call it when sending the response to the cloud
    :type cloud_inter: mqtt_interaction_cloud
    :param node id: node id to who we wish to communicate
    :type node id: int
    :param gw_id: gateway id that creates the tunneling
    :type gw_id: int
    :param msg_type: Message type of the message the cloud sent and we want to tunnel to the node
    :type msg_type: int
    :param msg_args: additional message arguments
    :type msg_args: list
    :param sink_id: Sink id where nodes connect to the gateway
    :type sink_id: string


    :does:
        1. Receives a series of message parameters from a gateway-cloud interaction
        2. Creates a temporal gateway-node interaction, and passes on the message
    
    :structure:
        1. It has the following methods:
            - :py:meth:`~interaction_tunnel.cloud_to_node_tunnel.transmit_message_to_node`   

    :return:

        Returns a :py:meth:`~mqtt_interaction_node_temporal.mqtt_interaction_node_temporal` class:

            :to_node_inter: (mqtt_interaction_node_temporal) -- gateway to mesh network interaction of class that the tunnel will create.   
            
    """


    def __init__(self, msg_type, msg_args, cloud_inter ) :
        """
        Initialize class interaction attributes.    
        """
        prefix = "<init cloud to node tunnel> "
        self.msg_type = msg_type
        self.node_id = cloud_inter.node_id
        self.gw_id = cloud_inter.gw_id
        self.sink_id = cloud_inter.sink          # this needs to be changed for production
        print(prefix + "msg type: {}, node id: {}, gw_id: {}, sink_id: {}".format(self.msg_type, self.node_id, self.gw_id,
                                                                                 self.sink_id ))
        self.to_node_inter = mqtt_interaction_node_temporal.mqtt_interaction_node_temporal(mode="request", wni= cloud_inter.wni)
        self.args = msg_args
        self.cloud_inter = cloud_inter

        # file for storing messages
    
    
        
    def transmit_message_to_node(self, prefix=""):
        """
        Function responsible for sending the message to the mesh network, the final step in the cloud --> node tunnel. 
        
        :does:
            1. Sends a node request. Originally, this is determined by the cloud request received by the gateway.
            2. The :py:meth:`~mqtt_interaction_node_basic.mqtt_interaction_node_basic.request_to_node` function creates a listening thread, for incoming node messages (possible responses to the previous request)
            3. We create a **thread.join()** which stops any further tunnel execution, until the right response is received or the max waiting time is achieved.
            4. If a matching response is received, we return True + the node message response. Otherwise we just output a log message notifying the lack of response.
            5. In order to respond to the cloud, we will call the :py:meth:`~interaction_tunnel.cloud_to_node_tunnel.respond_to_cloud` using the response message from the node, with a modified topic and id.

         :return:
            **result** (*list*) --  
                - [0] - *bool* (True if tunnel to node was successful, False if failed)
                - [1] - *RxMsg* node response message, or *None* if no message response.

        """
        prefix = prefix + "send to node>: "
        print(prefix + "sending cloud-received-message to node")
        result = [False, None]

        if self.msg_type in gvar.MSG_CLOUD_TO_NODE_REQUESTS_LIST: # things that can be asked from cloud to the nodes:
            self.to_node_inter.request_to_node(self.gw_id, self.sink_id, self.node_id, self.msg_type, self.args)
            print(prefix + "tunnel message sent to node.")
            self.to_node_inter.thread.join() # wait until we receive the right response to the request to the nodes, before continuing execution
            
            msg = RxMsg()
            
            if self.to_node_inter.pub_resp_received:
                msg = self.to_node_inter.node_response
                
            else:
                print(prefix + " error: node unresponsive")
                msg.type = gvar.MSG_TYPE_ERROR
                msg.args = [gvar.ERROR_TYPE_UNRESPONSIVE_NODE]
                # msg.payload = cmsgf.message_to_bytes(msg.id, msg.type, [gvar.ERROR_TYPE_UNRESPONSIVE_NODE], pubtopic=self.cloud_inter.pubtopic, prefix=prefix)
                
            # the response message has no cloud topic, so we have to assign the topic from the cloud-gw interaction:
            msg.topic = self.cloud_inter.subtopic  # we set the cloud subscription topic where we received the cloud request, so that the clo0ud response is created proprely

            # self.respond_to_cloud(msg) # now we can respond to the cloud
            result = [True, msg]

        elif self.msg_type in gvar.MSG_SUPPORTED_LIST_CLOUD: # cases that the gateway should answer itself to the cloud about the specific node
            result = [True, None]
        else:
            print(prefix + "msg type not in supported list")

        return result
    
   
def tunnel_to_node(cloud_inter, msg, wni=None):
        """
        Prepares the message the cloud wants to send to the node. It also sends the message and reports the response.
       
        :Note: When the gateway receives a cloud request to get the node version, it won't send a command directly to the node but it will send an
        OTAP command to the sink, asking for the scratchpad of that node, which will contain the node version.

        :does:

            1. Checks whether the cloud message is targeted towards a node or the gateway itself.
            2. If it is aimed at a **node**, then it can be either for 

                - getting the node version (in which case a direct otap message to the sink is sent)
                - Anything else, for which a :class:`cloud_to_node_tunnel <interaction_tunnel.cloud_to_node_tunnel>` class is created, 
                  and the message is sent to the node using the :py:meth:`~interaction_tunnel.cloud_to_node_tunnel.transmit_message_to_node`

            3. If the message is targeted towards the gateway, then no tunnel to the node is needed, and *None* is sent back to the cloud
            4. A few seconds after the message is sent to the node, a response message is received.
            5. The response from the node is returned together with a boolean (True/False) that determines if the tunnel to the node was
               successful or not.

        :param cloud_inter: cloud interaction of the gateway. We need to pass the whole interaction in order to allow the tunnel to call it when the node sends the response back to the cloud
        :type cloud_inter: mqtt_interaction_cloud
        :param msg: the message received
        :type msg: RxMsg
        :param wni: wirepas interface, we need it in order to create the otapHelper and requests node information to the sink directly
        :type wni: WirepasNetworkInterface  

        :return:
            - **result** (*list*)  
                - [0] - **Success** *(bool)* -- (True if successful, False if failed)
                - [1] - **Response msg** *(RxMsg)* -- response message from the node. Or error message, or None if no tunnel is needed.
        """
        
        prefix  = "<tunneling to node> "    
        sub_supertopic = gvar.get_supertopic(cloud_inter.subtopic)
        print("{} sub_supertopic: {} with gw id: {}".format(prefix, sub_supertopic, cloud_inter.gw_id))

        result = [False, None]

        if sub_supertopic == gvar.CLOUD_REQUEST_TO_NODE_MQTT_SUPERTOPIC: 
            if msg.type == gvar.MSG_TYPE_CLOUD_TO_NODE_GET_VERSION:
                # we dont need a direct tunnel to the node, because using otap we can directly ask the sink
                # the node version, and she will answer properly
                # ask nodes directly via sink (without expecting a node response) what is the node version
                # I put this in "read database" section because there was no other place I could put this.
                prefix = prefix + " node version> "
                print(prefix + "extracting node version...")
                # the otap needs the otaphelper in order to work :( )
                otapHelper = WirepasOtapHelper(wni,
                                    int(gvar.NETWORK_DEFAULT_CHANNEL))

                result = remotap.get_node_version( otapHelper, msg.node_id)
                print("{} node version: {}".format(prefix, result[1]))
            else:
                # tunnel message to nodes for ALL cloud > node messages, except the node version. For that we don't 
                # need a cloud > node tunnel:
                # call for sending node info if response is received
                tunnel = cloud_to_node_tunnel(msg.type, msg.args, cloud_inter)
                result = tunnel.transmit_message_to_node(prefix)

        
        # gateway receives a message for itself
        elif sub_supertopic == gvar.CLOUD_REQUEST_TO_GATEWAY_MQTT_SUPERTOPIC:
            prefix = prefix + "cl req to gw> "
            print(prefix + "no tunnel needed right now")
            #gateway process. i.e. conulst database and issue cloud response 
            result = [True, None]

        elif sub_supertopic in gvar.SUPERTOPIC_LIST:
             prefix = prefix + "other> "
             print(prefix + "no tunnel expected")
             result = [True, None]
        else:
             print(prefix + "error: no supertopic found!")

        return result


class node_to_cloud_tunnel:
    """ 
    Class that subscribes the gateway to a global MQTT topic for receiving messages to a specific node.
    This occurs when an unregistered node sends a message to the gateway.
    
    :does:
        1. Once it's invoked, it creates a :py:meth:`~mqtt_interaction_cloud.mqtt_interaction_cloud` class that will subscribe to the 
           right MQTT topic in the global broker.
        2. Every time a cloud message is received in this topic, it will transmit it to the node.
   
        
    :param cloud_inter: cloud interaction with the gateway created by node tigger.
    :type cloud_inter: mqtt_interaction_cloud
    :param node_id: node id to who we wish to receive the message from the cloud
    :type node_id: int
    :param pubtopic: Publish topic for the cloud interaction. Where should the gateway send its messages to?
    :type pubtopic: string
    :param subtopic: Subscription topic for the cloud interaction. Where should the gateway listen to for cloud messages?
    :type subtopic: string
    
    :return:

        Returns a :py:meth:`~interaction_tunnel.node_to_cloud_tunnel` class with the following attributes:

            :to_node_inter: (mqtt_interaction_cloud) -- gateway to mesh network interaction of class that the tunnel will create.   
            
    """
    def __init__(self, node_id, wni ):
        """
        Initialize class interaction attributes.    
        """
        prefix = "<init node to cloud tunnel> "
        self.node_id = node_id
        self.subtopic = gvar.CLOUD_REQUEST_TO_NODE_MQTT_SUPERTOPIC + str(self.node_id)
        self.pubtopic = gvar.GATEWAY_RESPONSE_TO_CLOUD_REQUEST_TO_NODE_MQTT_SUPERTOPIC + str(self.node_id)
        print(prefix +" node id: {}, subtopic: {}, pubtopic: {}".format(self.node_id, self.subtopic, self.pubtopic))
        self.cloud_inter = mqtt_interaction_cloud.mqtt_interaction_cloud(mode="listen", subtopic = self.subtopic, 
                                            pubtopic = self.pubtopic, wni = wni)
        # file for storing messages

def tunnel_to_cloud(node_id, wni):
        """
        Starts a cloud MQTT subscription for a desired node. 
        This interaction is triggered when the gateway receives a messages from an unregistered node.

        What it does:

            1. Creates a :class:`node_to_cloud_tunnel <interaction_tunnel.node_to_cloud_tunnel>` class.
            2. Starts the cloud interaction listening thread to recieved any cloud messages designed to this node

        :param node_id: id of the node that should receive the cloud messages
        :type node_id: int
        :param wni: wirepas interface, we need it in order to create the otapHelper and requests node information to the sink directly
        :type wni: WirepasNetworkInterface  

        :return:
            **result** (*list*)  
                - [0] - *bool* -- (True if successful, False if failed)
                - [1] -  :class:`mqtt_interaction_cloud <mqtt_interaction_cloud.mqtt_interaction_cloud>` -- mqtt interaction class with the cloud, the whole class is passed.

        """
        prefix  = "<tunneling to cloud> "    
        result = [False, None]

        try:
            print("\n{} Creating cloud tunnel for node {} ...".format(prefix, node_id))
            cloud_tunnel = node_to_cloud_tunnel(node_id, wni)      
            print("{} Tunnel set, starting a new thread to listen to cloud".format(prefix))      
            cloud_tunnel.cloud_inter.start_listen_thread()

            result = [True, cloud_tunnel.cloud_inter]

        except:

            print("{} tunneling to cloud failed.".format(prefix))
        
        return result

def prepare_cloud_tunnel(msg, node_inter):
    """
        Checks if the node that sent the message is registered or not and acts accordingly.

        :does:
            1. Checks if the node that sent the message is registered or not. 
            2. If the message comes from an unregistered node, a MQTT cloud subscription will be created via the 
        function :py:meth:`~interaction_tunnel.tunnel_to_cloud`.

        :param node_inter: main node interaction of the gateway. We need to pass the whole interaction in order to allow the tunnel use the node id for the subscription
        :type node_inter: mqtt_interaction_node_main
        :param msg: message received from the nodes
        :type msg: RxMsg

        :return:
            **result** (*list*)  
                - [0] - *bool* -- (True if successful, False if failed)
                - [1] - :py:meth:`~mqtt_interaction_cloud.mqtt_interaction_cloud`/*None* -- if a tunneling to the cloud is needed,
                  it passes the whole :py:meth:`~mqtt_interaction_cloud.mqtt_interaction_cloud` class.
                  Otherwise, it returns *None*.

    """
    prefix="<prepare cloud tunnel> "
    node_id_list = node_inter.node_id_list

    if msg.node_id not in node_id_list:
        print("{} creating tunnel to cloud".format(prefix))        
        cloudtunel = tunnel_to_cloud(msg.node_id, node_inter.wni)
    else:
        print("{} no tunnel to cloud needed".format(prefix))
        cloudtunel = [True, None]
    
    return cloudtunel



