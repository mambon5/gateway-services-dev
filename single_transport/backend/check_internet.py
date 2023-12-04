"""
Script to constantly check whether this computer has internet access or not.
If not, then restart all gateway services.
Timeout is for 5 seconds I believe.

"""

import sys
import time
import subprocess
import mqtt_credentials as creds
from requests import get

def restart_gw():
    """
    Restart gateway function
    """
    print("Internet connection lost :(, restarting gateway basic services...")
    subprocess.run("echo admin | sudo -S systemctl restart gateway_services.service", 
                   shell=True, capture_output=True, text=True)

def ping():
    status = True
    first = True
    while(status):
        if network_connection() is True:
            if first:
                print("all good and connected! :)")
                first=False
        else:
            restart_gw()
            status = False

        time.sleep(2)  #use 100 milliseconds sleep to throttke down CPU usage
    

def get_host(hostname=None, timeout=5):
        """
        pings a host with a certain timeout, and returns True if response was ok and within timeout, otherwise returns False.
        
        """
        prefix = "<get host>"

        if hostname == None:
            hostname = "http://{}".format(creds.global_broker)
        timeout = str(timeout)
        try:
            get(hostname,timeout)
            is_up = True
        except:
            is_up = False

        return is_up

def network_connection( timeout=5):
    """
    tries to get any of the following 3 servers via http/s and returns true if at least one of them works, false otherwise:

    1. http global server of salvi
    2. https global server of salvi
    3. google.com

    :param timeout: number of seconds to wait before timing out and considering this connection as failed. 
    :type timeout: int

    :returns:
        :connection: (bool) -- True if connection was successful with any of the tried hostnames, false if it failed or timed out in all of them

    """
    try:
        get_host(hostname="httsp://{}".format(creds.global_broker), timeout=timeout)
        return True
    except:
        try:
            get_host(hostname="httsps://{}".format(creds.global_broker), timeout=timeout)
            return True
        except:
            try:    #try with google
                get_host(hostname="https://www.google.com/", timeout=timeout)
                return True
            except Exception as error:
                print("couldn't get any hostname via http/s, error: {}".format(error))
    
    return False



def timeout_tests():
    """
    Pinging the global broker and Github, to check the latency and decide whether to uptade the code or not.
    :does:
        1. ping global broker with 2 and 4s timeouts. At least one must be passed
        2. Ping Github with 2 and 4s timeouts. At least one must be passed
        3. returns True/False if timeout tests are passed.

    :returns:
        1. True or False -- True if all timeout tests are passed, False otherwise


    """

    prefix = "<timeout tests>"
    host  = "http://159.223.30.89"

    try:
        timeo = 0.001
        network_connection(host, timeo)
        print("{} reaches global broker within {} sec".format(prefix, timeo))
    except:
        try:
            timeo = 0.001
            network_connection(host, timeo)
            print("{} reaches global broker within {} sec".format(prefix, timeo))
        except Exception as error:
            print("{} reaches global broker within {} sec".format(prefix, timeo))
            return False

    host  = "https://github.com/"
    try:
        timeo = 0.001
        network_connection(host, timeo)
        print("{} reaches Github within {} sec".format(prefix, timeo))
    except:
        try:
            timeo = 0.001
            network_connection(host, timeo)
            print("{} reaches Github within {} sec".format(prefix, timeo))
        except Exception as error:
            print("{} reaches global broker within {} sec".format(prefix, timeo))
            return False
        
    return True



def check_delay():
    p = subprocess.Popen(["ping","www.google.com"], stdout = subprocess.PIPE)
    res = p.communicate()[0]
    res.split("\n")

def main(mode=1):
    """
    Check once for internet connection syncronously or asyncronously, depending on the selected mode.

    mode == 1: creates an asynconronous continuous loop
    mode == 2: check syncronously the internet connection, and blocks execution until internet connection is resolved
    """
    
    if mode == 2: # check syncronously the internet connection, and blocks execution until internet connection is resolved
        if network_connection():     
            print("all good and connected! :)")
        else:
            restart_gw()
     # asynconronous continuous loop
    else:
        ping()
         
    


if __name__ == "__main__":    
    prefix = "<check internet>"
    try:
        mode = sys.argv[1] # prints python_script.py
    except: 
        mode = 1
    print("{} selected mode: {}".format(prefix, mode))
    main(int(mode))





