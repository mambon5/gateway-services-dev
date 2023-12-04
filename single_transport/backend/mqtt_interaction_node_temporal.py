"""MQTT interaction class of gateway and mesh network created for a short period of time.
 When a cloud message is received a tunneling is created towards the specific node. This means this class is created to allow
 a direct interaction from the gateway to the node in question. Once the message is received from the node, this class is terminated.
 """

from mqtt_interaction_node_basic import mqtt_interaction_node_basic

class mqtt_interaction_node_temporal(mqtt_interaction_node_basic):
    """    
    This is the temporal interaction class with the nodes. It helps bridge the cloud messages to its nodes
    
    :structure:
        1. This class is created every time the gateway receives a cloud message for a node, and destroyed once it delivers the message to the 
           desired node. It only exists for a brief period of time.
        3. It is the last step in delivering a cloud message to a node.
        4. It has the following methods:
            - :py:meth:`~mqtt_interaction_node_temporal.mqtt_interaction_node_temporal.on_message_temporal_node`

    :param interlocutor: entity which we wish to communicate to. Defaults to *cloud*
    :type interlocutor: string

    :return:

        Returns a :py:meth:`~mqtt_interaction_node_basic.mqtt_interaction_node_basic` class with the following attributes:

            :node_id: *(int)* -- node id or node address where the message has to be sent to
    """

    def __init__(self, mode="request", wni=None, node_id=None):

        prefix = "<init mqtt node interac> "
        self.node_id = node_id
        
        mqtt_interaction_node_basic.__init__(self, mode=mode, wni=wni)       

        prefix = "<mqtt_interaction_node_temporal innit>: "

    def on_message_temporal_node(self, msg, timestamp):
        """
        This function gets called when a node that received the cloud instruction, sends its response back to the gateway.
        Basically the temporal node interaction should:
            - check if the message matches a previous gateway request
            - if it matches, then save the response message (in order to pass it back to the cloud later on)
     
        """
        prefix = "<on message temporal node> "
        print(prefix +"possible response received at {} : node: \n{}, payload: {}\n".format(timestamp, msg.node_id, msg.payload))
            
        if self.check_for_response(msg):
            # if the message received is the response, then store it accordingly for tunneling back to cloud
            self.node_response = msg

   


    

    