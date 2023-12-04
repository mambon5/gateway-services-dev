"""
Here we specify and store all the broker settings. Both the settings to the local and the cloud MQTT broker
"""
#: connection to local MQTT broker settings:
local_broker="127.0.0.1" # local server 
# local_broker="test.mosquitto.org" #: free online server

# broker="159.223.30.89" # Alice's server
local_port=1883    #: local port
# local_user="roma_masana"
# local_password="all_I_want_for_christmas_is_you"
local_insecure=True

# connection to local MQTT broker settings:
# global_broker="127.0.0.1" #: local server 
# global_broker="91.126.33.138" #: Alice's server
global_broker="159.223.30.89" #: Alice's server
# global_broker="209.38.235.149" #: Alice's server 2
# global_broker="test.mosquitto.org" #: free online server
# global_broker="91.121.93.94" # mosquitto org ip address
# global_broker="st.salvilighting.com"
global_port=1883
# global_port=8080
# global_user="roma_masana"
# global_password="all_I_want_for_christmas_is_you"
global_insecure=True


def get_local_creds():
    """
    Generate the local credentials and send them, based on the set values.

    :returns:
        - :local_user: (*string*) -- if set, username to access the local MQTT broker
        - :local_password: (*string*) -- if set, password to access the local MQTT broker
        - :global_insecure: (*bool*) -- allow insecure connections?
    """
    global global_insecure
    # connecting to wirepass mesh network
    try: local_user
    except:
        local_user = None
        local_password = None

    try: global_insecure
    except:
        global_insecure= True
    
    return([local_user, local_password, global_insecure])

def get_global_creds():
    """
    Generate the global credentials and send them, based on the set values.

    :returns:
        - :global_user: (*string*) -- if set, username to access the global MQTT broker
        - :global_password: (*string*) -- if set, password to access the global MQTT broker
        - :global_insecure: (*bool*) -- allow insecure connections?
    """
    try: global_user
    except:
        global_user = None
        global_password = None

    try: global_insecure
    except:
        global_insecure= True

    return([global_user, global_password, global_insecure])