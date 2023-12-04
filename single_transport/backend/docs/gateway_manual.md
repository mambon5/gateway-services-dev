

- [How to install the gateway's software](#how-to-install-the-gateways-software)
  - [1. Downloading Linux OS and saving it into an USB](#1-downloading-linux-os-and-saving-it-into-an-usb)
  - [3. Installing a Linux (ubuntu) OS](#3-installing-a-linux-ubuntu-os)
    - [If using Linux and your USB bootable drive is not detected (20min)](#if-using-linux-and-your-usb-bootable-drive-is-not-detected-20min)
    - [Linux installation configuration (45min)](#linux-installation-configuration-45min)
  - [4. Disable linux system from automatically updating (10min)](#4-disable-linux-system-from-automatically-updating-10min)
    - [Remove all update software](#remove-all-update-software)
    - [Also set up don't show update notifications:](#also-set-up-dont-show-update-notifications)
  - [5. Disable automatic session logout and the password prompt on startup (10min)](#5-disable-automatic-session-logout-and-the-password-prompt-on-startup-10min)
  - [6. Install basic linux apps and pip packages: (23min)](#6-install-basic-linux-apps-and-pip-packages-23min)
    - [Install mosquitto configuration files (20min)](#install-mosquitto-configuration-files-20min)
  - [7. Download github code (25min)](#7-download-github-code-25min)
  - [8. Give your gateway an id](#8-give-your-gateway-an-id)
  - [9. Create two `systemd` linux service to start the gateway and a timer](#9-create-two-systemd-linux-service-to-start-the-gateway-and-a-timer)
    - [1. The *gateway services* service (20min)](#1-the-gateway-services-service-20min)
    - [2. The *gateway update code* service  (20min)](#2-the-gateway-update-code-service--20min)
    - [3. Set up a timer to update the gateway periodically  (10min)](#3-set-up-a-timer-to-update-the-gateway-periodically--10min)
  - [10. Cap the logs of journalctl and syslog](#10-cap-the-logs-of-journalctl-and-syslog)
    - [Caping the journal logs](#caping-the-journal-logs)
    - [Delete the system logs (only if logs are already huge \> 1GB )](#delete-the-system-logs-only-if-logs-are-already-huge--1gb-)
  - [11. Give user permissions to the logs](#11-give-user-permissions-to-the-logs)
  - [12. Add the username to the sudoers file:](#12-add-the-username-to-the-sudoers-file)
  - [13. Plug in sink and reboot](#13-plug-in-sink-and-reboot)
- [How does the gateway communicate with the cloud and node?](#how-does-the-gateway-communicate-with-the-cloud-and-node)
  - [Message format](#message-format)
  - [Cloud to gateway messaging](#cloud-to-gateway-messaging)
    - [MQTT topics:](#mqtt-topics)
      - [Notes](#notes)
  - [Message content](#message-content)
    - [Explanation of the message fields:](#explanation-of-the-message-fields)
    - [Message types and arguments](#message-types-and-arguments)
      - [Cloud to node messages](#cloud-to-node-messages)
      - [Cloud to gateway messages](#cloud-to-gateway-messages)
      - [Gateway to cloud messages](#gateway-to-cloud-messages)
    - [Possible errors](#possible-errors)
- [How to use the gateway backend API](#how-to-use-the-gateway-backend-api)
  - [Taking remote control of the gateway](#taking-remote-control-of-the-gateway)
  - [Gateway details](#gateway-details)
    - [List of gateways ever connected to the local broker](#list-of-gateways-ever-connected-to-the-local-broker)
  - [Changing the sink configuration](#changing-the-sink-configuration)
- [How does the gateway's backend API code work?](#how-does-the-gateways-backend-api-code-work)
  - [Notes](#notes-1)
  - [How is the Gateway's id number chosen?](#how-is-the-gateways-id-number-chosen)
- [Connectivity tests](#connectivity-tests)
  - [1. Barcelona lab](#1-barcelona-lab)
  - [2. Dammam](#2-dammam)

# How to install the gateway's software

**Estimated time to complete installation**: **2h40min** if it is the first time. 
1. Download a Linux OS version into an USB (40min)
2. Start the PC and configure the basic settings in Windows in order to reboot from a usb (15min)
3. Install the Linux OSystem: (40min) 
4. Disable automatic updates of the Linux software (5min)
5. Disable automatic session logout and the password prompt on startup (5min)
6. Install basic software and python packages for running the gateway (25min)

7. Clone the Github repo, enter the valid credentials and download all the code (5min)
   1. create a directory called `smartec` under `/home/salvi-smartec` in your PC
   2. clone the Github repository using 
    ```
    git clone https://github.com/smartec-lighting/gateway-services.git
    ```
    into the folder of the last point.
8. Install linux systemd services, enable them, and run `sudo systemctl daemon-reload` to save the changes. (25min)
9. Reboot the computer in order to start the service that updates the gateway's code. (3min)


## 1. Downloading Linux OS and saving it into an USB

I installed Linux Ubuntu 22.10 version.

This tutorial describes all the required steps to complete this operation > https://ubuntu.com/tutorials/create-a-usb-stick-on-windows#1-overview

Once you complete it, you will have an USB drive, with the Linux system inside and ready to be installed into a Windows PC.

## 3. Installing a Linux (ubuntu) OS

Insert the USB stick into the PC's USB port, and reboot the PC to start the Linux boot menu. Alternatively, use the windows advanced startup options to immediately reboot the PC and start the Linux boot menu. However you do it, you should manage to start the linux boot menu, and select *Install Linux*.

### If using Linux and your USB bootable drive is not detected (20min)

If you are using Linux and your USB bootable drive is not detected automatically on system reboot or startup, then you
have to enter the GRUB interface and find the usb and boot it manually. In order to do so, check the following guide > https://linuxhint.com/boot-usb-using-grub/

Basically:
1. Enter GRUB (by pressing Esc on Ubuntu startup)
2. Press Esc again in order to enter the GRUB terminal
3. list all the drives by running `ls`
4. set the root to one of the drives by running
```
set root=(hd0,msdos5)
```
5. Try to execute the supposedly bootable efi file inside by running:
```
chainloader /efi/boot/grubx64.efi
```
6. If you obtain a `failure` result, try with a different drive or hard disk and repeat setps 4-5. Once you find one that gives a result different than `failure` you probably found and set the right usb drive for booting.
7. Now boot form it by running:
```
boot
``` 

### Linux installation configuration (45min)

I am using Linux Ubuntu Server 22.10. 

During the installation process:

1. During linux Installation I select *minimal installation*

2. For **desktop configuration:**
   1. I Select **Do not update or download any updates after installation** to avoid any future software incompatibilities.
   2. I chose *delete hardisk*, and install Ubuntu in order to earase any other OS.
   3. Do not choose any advanced option, a LVS volume manager or a ZFS filesystem won't be as fast as the default EXT4 filesystem which is what we want installed. I always did the installation with the EXT4 (default) filesystem.
   4.  Press *Continue* and *Install* Linux.
   5.  **important step** -> Select the following username and password:
      1. user: **salvi-smartec**
      2. password: **admin**
   6.  Choose **start session automatically** in order to avoid asking for the password on system reboot.
   
<!-- 3. Alternatively, for Server configuration (recommended for speed):
   1. **Network connections** > leave the default networks that the computer detected.
   2. **Proxy and mirror** > leave the default configuration of the proxy server and mirror address.
   3. **Update the new installer** > Select *Continue without updating*
   4. On **Guided storage configuration** > Select *Use an entire disk*
   5. On **Storage configuration** > Leave the default settings and click *Done*
   6. Press *Continue* and *Install* Linux.
   7.  User credentials **important step** -> Select the following username and password:
       1. user: **salvi-smartec**
       2. password: **admin**
   8.   On the **SSH Setup** choose the following:
        - Install OpenSSH server
        - Import SSH identity from Github
        - Enter the gateway *github credentials*
        - Press OK then the public SSH key should be displayed:
        ```
        SHA256:rqPljnsn+kcqPalbUr2TEWiFw95Gk3EhS5lvW4XfE54
        ```
        - Then choose *Yes* to use this SSH key.
    9. Skip the next screen where you can choose new linux packages, and the installation will start automatically
    10. Once the installation is complete, press **skip automatic/security updates** to avoid any updates from being installed.
    11. Install the *nano* package by running:
    ```
    sudo apt-get install nano
    ```
    12. If on server startup the server takes 2min waiting for network configuration, consider doing the following > https://askubuntu.com/questions/1321443/very-long-startup-time-on-ubuntu-server-network-configuration -->


## 4. Disable linux system from automatically updating (10min)
 
Open a Linux terminal on your PC that will work as the gateway. Then run:

```
sudo nano /etc/apt/apt.conf.d/20auto-upgrades
```
and change these two lines:

```
APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Unattended-Upgrade "1";
```

For these four:

```
APT::Periodic::Update-Package-Lists "0";
APT::Periodic::Download-Upgradeable-Packages "0";
APT::Periodic::AutocleanInterval "0";
APT::Periodic::Unattended-Upgrade "0";
```

### Remove all update software

here is described all that should be uninstalled and disabled > https://askubuntu.com/questions/1322292/how-do-i-turn-off-automatic-updates-completely-and-for-real

In particular, delete the upgrade software by running the following:

```
sudo apt remove unattended-upgrades
```

```
sudo apt remove update-notifier
```

```
sudo apt remove update-manager
```

I also removed snap-store:

```
$ sudo snap remove snap-store 
```

### Also set up don't show update notifications:

By running this command:

```
gsettings set com.ubuntu.update-notifier no-show-notifications true
```

## 5. Disable automatic session logout and the password prompt on startup (10min)

1. Disable automatic session logout > You should navigate to **Setting > Privacy >  Screen Lock > Automatic Screen Lock (Off)**
2. **For desktop installation** > You have to *Enable the automatic login* of the linux system as described here > https://linuxconfig.org/how-to-enable-automatic-login-on-ubuntu-18-04-bionic-beaver-linux 
<!-- 3. Alternatively, for **server installation** > In the case you installed the Server version of linux, do the following:
   
   1. in particular, do as explained in this guide > https://ostechnix.com/ubuntu-automatic-login/, basically:
   2. Run `sudo nano /etc/systemd/logind.conf` and uncomment the line s
   ```
   NAutoVTs=6
   ReserveVT=7
   ```
   Save and exit.
   3. Then run `sudo systemctl edit getty@tty1.service` and write this code inside:
   ```
   [Service]
    ExecStart=
    ExecStart=-/sbin/agetty --noissue --autologin ostechnix %I $TERM
    Type=idle
   ```
    Save and exit.
    4. Reboot  -->


## 6. Install basic linux apps and pip packages: (23min)

Install new packages (optional or not recommended I still don't know):
```
sudo apt-get update
sudo apt-get upgrade
```

Install the following linux packages:
```
    sudo apt-get update
    sudo apt install nano
    sudo apt install git
    sudo apt install docker-compose
    sudo apt install mosquitto
    sudo apt install mosquitto-clients
    sudo apt install python3-pip
    sudo apt install setserial
  ```
Install the following *pip-python* packages:
```
    pip3 install numpy
    pip3 install wirepas-mqtt-library
    pip3 install wirepas-mqtt-library --upgrade
    pip3 install paho-mqtt python-etcd
    pip3 install getmac crc
```

**Note**: Check that the installed version for `wirepas-mqtt-library` is 1.2, and if not, run the following commands to upgrade it:

```
sudo apt-get update
pip3 install wirepas-mqtt-library --upgrade
```


### Install mosquitto configuration files (20min)

Set up a `/etc/mosquitto/conf.d/default.conf` file with the following content:

```
listener 1883 
allow_anonymous true 
```

This will tell the mosquitto server to listen to port 1883 locally, for incoming connections, and to allow anonymous traffic.


## 7. Download github code (25min)
From https://github.com/smartec-lighting/gateway-services .

In particular:

1. If you set up your linux username as explained before, you should now have the following folder: 
```
/home/salvi-smartec/
```
2. If that is not the case, reinstall linux and start from steps 3 again once you see this folder. 
3. If you already have this folder, then go into this directory, and create a folder called:
```
/home/salvi-smartec/smartec/
```
4. Now `cd` into `smartec` and you are almost ready to download all the github code.

5. Github account credentials to use in the gateway
 You should use the following Github credentials:

- Username: SmartGWay
- email: smartec@salvi.es
- Password: Smartec.23
- token: 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
  
6. Before downloading all the github code, we will set the PC to remember its github credentials for later use, by running the following commands:
    1. First run this command to tell git to remember your credentials:
        ```
         git config --global credential.helper store
        ```
     2. run these commands to enter your credentials:
        ```
         git config --global user.name 'SmartGWay'
         git config --global user.password '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'
         git config --global user.token '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'
        ```
7. Now we can finally clone the *production* github code, by doing `cd` inside the directory `smartec` and then run:
   ```
    git clone https://github.com/smartec-lighting/gateway-services-production.git
   ```
    This will create the directory 
    ```
    /home/salvi-smartec/smartec/gateway-services-production
    ```
    For the gateway software to work, move this directory to 
    ```
    /home/salvi-smartec/smartec/gateway-services
    ```

Now all the github code should be properly downloaded into the right directory in the gateway.


## 8. Give your gateway an id

It is now the moment of running the shell script:

```
cd smartec/gateway-services/single_transport
./install_docker_services.sh
```
and *enter a unique gateway id number*. This number that you will enter will be saved in the gateway docker files until you manually change it again.

Be careful with this step, since no two gateways with the same id can connect to the same global MQTT broker.

## 9. Create two `systemd` linux service to start the gateway and a timer

In order to automatically start and update the gateway code on reboot, two linux `systemd` services need to be created for the OSystem on `/etc/systemd/system/`. Additionally, a linux timer can be set up, in order to periodically update the gateway's code, for instance.

These services are the following:


### 1. The *gateway services* service (20min)

In order to start the gateway service on reboot, create a *gateway_services.service* file on `/etc/systemd/system/` by running

```
sudo nano /etc/systemd/system/gateway_services.service
```
with the following code:

```
[Unit]
Description="Smartec gateway services"
Wants=network.target
After=network-online.target

[Service]
Type=simple
ExecStart=/home/salvi-smartec/smartec/gateway-services/single_transport/backend/start_gateway_services.sh >> /home/salvi-smartec/smartec/gateway-services/single_transport/backend/logs/gateway_services_logs_1.log
Restart=on-failure
RestartSec=60
KillMode=control-group
User=salvi-smartec
StandardOutput=append:/home/salvi-smartec/smartec/gateway-services/single_transport/backend/logs/gateway_services_logs_1.log
StandardError=append:/home/salvi-smartec/smartec/gateway-services/single_transport/backend/logs/gateway_services_logs_2.log

[Install]
WantedBy=multi-user.target  
```

Remember to save the edits after you press Ctrl + X.

Now we must enable the service:
```
sudo systemctl enable gateway_services.service
```
And start it:
```
sudo systemctl start gateway_services.service
```
And update the system `daemon` if we make any change to the timer:
```
sudo systemctl daemon-reload
```

### 2. The *gateway update code* service  (20min)

We will create a `systemd` service called `gateway_update_code.service` that runs every day when the timer `gateway_update_code.timer` triggers and calls it, and updates from github all the gateway code.

the commands the this service will execute are in the script 
```
git_update_gateway_code.sh
```
(just for your information). The service is going to be called 
```
gateway_update_code.service
```
You can go ahead and execute the following in order to create the service:

```
sudo nano /etc/systemd/system/gateway_update_code.service
```

and add this to the service file:

```
[Unit]
Description="update gateway software via git"

[Service]
Type=simple
ExecStart=/home/salvi-smartec/smartec/gateway-services/single_transport/backend/git_update_gateway_code.sh
KillMode=control-group
User=salvi-smartec
StandardOutput=append:/home/salvi-smartec/smartec/gateway-services/single_transport/backend/logs/gateway_services_logs_1.log
StandardError=append:/home/salvi-smartec/smartec/gateway-services/single_transport/backend/logs/gateway_services_logs_2.log

[Install]
WantedBy=multi-user.target  
```
We need to run this service as *superadmin* or root, since the *.sh* file that we want this service to run, requires superadmin powers. We can either set `User=root` which will give *ownership issues* with the `git fetch --all` command when pulling the Github code, or we can better set *root privileges* for the local user *LOCAL_USER* by running:
```
sudo usermod -G root salvi-smartec
``` 

Now we must enable the service
```
sudo systemctl enable gateway_update_code.service
```
And start it
```
sudo systemctl start gateway_update_code.service
```
And update the system `daemon` if we make any change to the timer:
```
sudo systemctl daemon-reload
```

### 3. Set up a timer to update the gateway periodically  (10min)

To run this service periodically, we must set up a system timer. You can read more on how to set a system timer here > https://wiki.archlinux.org/title/systemd/Timers . Basically we have to create a timer (which is a *.timer* file), create the file by running:
```
sudo nano /etc/systemd/system/gateway_update_code.timer

```
The timer that will execute this service file must have the same name as the service, in this case it must be called
```
gateway_update_code.timer
```

And it must containg the following configuration (copy this into the timer file):
```
[Unit]
Description="update gateway software via git"

[Timer]
OnCalendar=*-*-* 12:00:00

[Install]
WantedBy=timers.target 
```
This will call the `gateway_update_code.service` service, every day at **12pm**. This will make sure the code is updated daily, and won't do the code update at nightime, when the lamps are on.

Now we must enable it 
```
sudo systemctl enable gateway_update_code.timer
```
And start it
```
sudo systemctl start gateway_update_code.timer
```
And update the system `daemon` if we make any change to the timer:
```
sudo systemctl daemon-reload
```

## 10. Cap the logs of journalctl and syslog

### Caping the journal logs
We need to cap the maximum size of the log file `journal` in order to avoid the service from writing too much information and making the device run out of disk space. Run this command to cap it to *500MB*:
```
sudo journalctl --vacuum-size=500M
```

### Delete the system logs (only if logs are already huge > 1GB )
You can check first the size of the system logs by running the command:
```
du -sh /var/log/syslog.1
```
If they exceed the 500MB or 1GB, then I recommend you erase them, by following the next steps. 
Run:
```
sudo -i
```
Then run the remove command, in my case:
```
> rm /var/log/syslog.1
```
Always make sure to exit your root shell once you're done with it
```
exit
```

## 11. Give user permissions to the logs

It is a common error that I encounter, the fact that some logs can't be edited by the trimming files `trim_log_output.sh`, because the trimming file doesn't have *root* permissions to the logs.

It is important then to create these files with just user permissions so they can be trimmed automatically and don't grow out of disk space.

In order to give root permissions to the user, follow this guide > https://linuxopsys.com/topics/give-normal-user-root-privileges?utm_content=cmp-true in particular, run:

```
sudo usermod -G root salvi-smartec
```
## 12. Add the username to the sudoers file:

If you find the following error: ** this webpage explains how to solve it > https://www.tecmint.com/fix-user-is-not-in-the-sudoers-file-the-incident-will-be-reported-ubuntu/ Basicall you have to:
1. Enter the startup option *ubuntu* for advanced options Grub menu by pressing *shift* on boot.
2. select `root` on the recovery menu and press *enter*
3. Go to *recovery mode* and press *enter* for *maintenance*.
4. Add the *salvi-smartec* to the *sudo* group by running
```
adduser salvi-smartec sudo
exit
```
and start the normal boot sequence.

## 13. Plug in sink and reboot

Finally, after all this is okay, plug in the sink usb device and reboot your pc. Now the gateway should be fully operational.

<!-- ## Install an OpenSSH server

If you want to be able to remotely control the gateway using SSH, you should install the OpenSSH server as described here, in the gateway > https://ubuntu.com/server/docs/service-openssh -->

# How does the gateway communicate with the cloud and node?

The gateway communicates with the **cloud server** and the **nodes**. The communications have three different kinds of nature for the gateway:

1. Sometimes it just passes a message from the cloud to the node, or viceversa
2. Others it creates a message intended for either the cloud or the nodes
3. It can also receive cloud messages or node messages intended exclusively for the gateway

We classify the messages in two different main **interactions**:

1. The messages the cloud and gateway exchange. The gateway calls this the **cloud** interaction or interlocutor.
2. The messages that the nodes and the gateway exchange. The gateway calls this the **nodes** interaction or interlocutor.

Within the gateway to **cloud** interaction, we further classify the messages depending on its origin and destiny like so:

1. **cloud --> node** 
2. **cloud --> gateway** 
3. **gateway --> cloud** 

And within the gateway an **nodes** interaction, we distinguish the following subtypes of messages:

1. **gateway --> node**  
2. **node --> gateway**  

Finally, we need to mention that for each message the cloud sends to the gateway for instance, another message needs to be sent back to the sender, *the response* so that whoever sent the message gets a confirmation or the requested information.

Thus, each message should be accompained by its response, and the scheme will look rather like this:

1. **cloud --> node** & its response
2. **cloud --> gateway** & its response
3. **gateway --> cloud** & its response

And within the gateway an **nodes** interaction, we distinguish the following subtypes of messages:

1. **gateway --> node**  & its response
2. **node --> gateway** & its response

This is the rough schema of the different type of gateway message communications and the main players in it. Let's not give more details of how this works.

## Message format

We are using the MQTT protocol to send information from the gateway to the nodes and to the cloud. This protocol has the format described here > https://www.bevywise.com/blog/understanding-mqtt-protocol-packet-format/ . In our case, we will talk only about the MQTT message **payload** but we will simply call it the *message*. In strict MQTT terms, what we call *message* is only a part of the message: the payload.

In our case, all the messages involving the gateway will be **formatted in bytes**, and in particular they will have the following format:

- **message id** | **message type** | **message arguments**
  
Where
  - The  **message id** is the unique message identifier, it will be an *unsigned integer* value stored with *2 bytes of memory*. The message id is just an identifier that will allow the receiver to send a response with the same message id, which in turn will allow the original sender to check which one is the response out of all the messages it might receive.
  - The  **message type** contains specific command information. Each message type implies a different action or information. The message type is also an *unsigned integer* that is stored in *1 byte of memory*. For instance a message with **type=1** tells a node to turn the led on, a **type=2** implies turn the led off, a message **type=14** means a new strategy is being sent to the node.
  - The **message arguments** contain additional information or parameters that need to be sent by the sender to the receiver. For instance the message **type=3** tells the node to set a dimming, the value of the dimming is sent as an argument, in this case a number 0-100. Other arguments could be a list of the nodes that the gateway has, or a new lighting strategy for the nodes, which would *need several bytes* to store. 


## Cloud to gateway messaging

The protocol we used in the cloud to gateway messaging is *MQTT*. In particular we set a specific *MQTT* topic for each message (and each response) in order to distinguish it clearly from each other.

### MQTT topics:

The different MQTT topics for each of the 3 request messages and its 3 responses are the following ones:

   - **cloud --> node**
     - request **cloud --> node** MQTT topic: `cl-req/n/<node_id>`
     - response **cloud <-- node** MQTT topic: `gw-res/n/<node_id>`
   - **cloud --> gateway** 
     - request **cloud --> gateway**  MQTT topic: `cl-req/gw/<gateway_id>`
     - response **cloud <-- gateway**  MQTT topic: `gw-res/gw/<gateway_id>`
   - **gateway --> cloud** 
     - request **gateway --> cloud** MQTT topics: `gw-req/gw-init/` and `gw-req/gw/<gateway_id>`
     - response **gateway <-- cloud** MQTT topic: `cl-res/gw/<gateway_id>`

#### Notes

The mosquitto_pub command sends the message payload in string only, so writing the payload in bytes and sending it as bytes via MQTT, will be read as string and therefore will use way more bytes than actually sent. The solution is to convert each byte into a character




## Message content

Here we describe the content of each message sent to each machine. The information includes the values sent, a short description, the number of bytes, and the information contained in each byte of the message.

Due to the limitation of **256MB** put on a MQTT message (http://www.steves-internet-guide.com/mqtt-broker-message-restrictions/), the maximum ammount of bytes in a message payload is around **268435455 bytes**, which limits the payload or number of nodes that can be added in a single message in some of the cases below. 


### Explanation of the message fields:


- The first term is the *message id* and has 2 bytes (H - unsigned long int)
- The second term is the *message type*. We only use 1 byte for this, therefore we have 256 different message types to use. In the gateway-backend to node communication we reserved the values 1-128 for gateway messages to node, and the numbers 129 to 255 for node messages to gateway. However, since each type of message has its own MQTT topic, this distinction is not necessary anymore, and all messages type can be encoded starting by 1 in each case.
- the third to the last term are *message arguments* that depend on the specific message type. Some messages have more arguments, some don't have any.
-  Each value of the message is encoded according to the format of the reference https://docs.python.org/3/library/struct.html. Each value must therefore be encoded in either **1 byte** (B,b), **2 bytes**(H), **4 bytes**(i,I) or **8 bytes**(q,Q) to be platform independent. 
- For more information on the mqtt packet format check https://openlabpro.com/guide/mqtt-packet-format/

**Note:** Notice that wirepass transforms the payload we send, and adds extra information such as 
- destination_address
- source_endpoint
- destination_endpoint
- qos
- payload *<-- the initial payload*
- initial_delay_ms *(if initial_delay_ms > 0)*
- is_unack_csma_ca *(if is_unack_csma_ca is True)*
- hop_limit *(if hop_limit > 0)*
For instance, if we just want to send a "send action" command from gateway to node, containing a message id of *1022* and a message type of *3* (3 bytes in total), the wirepass libraries end up sending around 33 bytes of message. Thus it appends around 30 bytes to each sent message in order to use the wirepass technology and ensure its optimal distribution.


###  Message types and arguments

#### Cloud to node messages

The process for this kind of messages is the following:

1. The cloud will send this message to the gateway
2. The gateway will take it, process it . If there is something wrong, the gateway will responde with an error to the cloud. If the processing
   is ok, then the gateway will send the message to the node and the process will continue as follows:
   1. The node will receive it, process it, and send a response to the gateway after processing it.
   2. Once the gateway receives the node response, the gateway will send a response to the cloud
3. The cloud will receive the gateway response.

In the following table we have the content, byte by byte, of each message that the cloud can send to a node through the gateway.

|message name   | description   |  Call  | bytes  | response | bytes  | cl-gw-n-test | 
|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|:-----------------:|:-----------------:|
|led on         | turn led on  |[  msg_id(H) msg_type= **1** (B) ]    |    3          |[  msg_id(H) msg_type= **1** (B) ]        | 3                 | OK-OK-OK-OK |
|led off        | switch led off| [  msg_id(H) msg_type= **2** (B) ]   |    3          |[  msg_id(H) msg_type= **2** (B) ]       | 3                | OK - OK - -OK-OK |
|dimming        | set dimming for led| [  msg_id(H) msg_type= **3** (B) dimming(b) ]   |    4          |[  msg_id(H) msg_type= **3** (B) dimming(b) ]       | 4                | OK - OK - OK - OK |
|blink        | start blinking|  [ msg_id(H) msg_type= **4** (B) ]   |    3          |[  msg_id(H) msg_type= **4** (B) ]       | 3                | OK -OK-OK -OK |
|strategy        | send a lighting strategy| [  msg_id(H) msg_type= **5** (B) strategy(B) ]   |    4          |[  msg_id(H) msg_type= **5** (B) strategy(B) ]       | 4                | OK - OK - node answers with strategy 21 always - OK |
|echo        | requests the  node to run an echo command        | [  msg_id(H) msg_type= **6** (B) ]   |    3          |[  msg_id(H) msg_type= **6** (B) traveltime(I) ]       | 7                | OK -OK-OK-OK |
|led status        | requests led status        |[  msg_id(H) msg_type= **7** (B) ]   |    3          |[  msg_id(H) msg_type= **7** (B) let_status(B) ]       | 4        | OK -OK-OK-OK (node invents value)|
|dimming status        | requests dimming status        |[  msg_id(H) msg_type= **8** (B)  ]   |    3          |[  msg_id(H) msg_type= **8** (B) dimming(b) ]       | 4                | OK -OK-OK -OK |
|neighbours        | requests number of neighbours        | [  msg_id(H) msg_type= **9** (B)  ]   |    3          |[  msg_id(H) msg_type= **9** (B) num_neighbours(I) ]       | 7                | OK -OK-OK -OK |
|rssi        | requests rssi status        |[  msg_id(H) msg_type= **10** (B)  ]   |    3       |[  msg_id(H) msg_type= **10** (B) rssi(b) ]       | 4       | OK -OK-OK -OK |
|hops        | requests number of hops, this request is answered by the gateway, not tunneled to the node        |[  msg_id(H) msg_type= **11** (B)  ]   |    3       |[  msg_id(H) msg_type= **11** (B) hops(B) ]       | 4       | OK-OK-OK -OK |
|node status        | requests all info from node        |[  msg_id(H) msg_type= **12** (B)  ]   |    3       |[ msg_id(H) msg_type= **12** (B) led_status(B) dimming(b) num_neighbours(I) rssi(b) hops(B)  ]| 11      | OK -OK-node invents led_status and dimming - OK |
|node software version | asks for node stack & app version        |[  msg_id(H) msg_type=**13** (B) ]   |    3       |[ msg_id(H) msg_type=**13** (B) version(BBBB BBBB) ]| 11       | OK - OK - OK - OK |
|new/modify strategy        | sends new strategy info    |[  msg_id(H) msg_type=**14** (B) strategy_id(H) {hour(B) minute(B) dimming(B)}·7  ]   |   26       |[ msg_id(H) msg_type=**14** (B) CRC{ whole payload }(I) ]| 7       | NO - NO - NO - NO |
|delete strategy        | deletes strategy    |[  msg_id(H) msg_type=**15** (B) strategy_id(H) ]   |    5      |[ msg_id(H) msg_type=**15** (B) strategy_id(H) ]| 5     | NO - NO - NO- NO |
|new/modify event        | sends new strategy info    |[  msg_id(H) msg_type=**16** (B) event_id(H) strategy_id(H) d_start(B) m_start(B) y_start(B) d_end(B) m_end(B) y_end(B) weekly(B)  ]   |   14       |[ msg_id(H) msg_type=**16** (B) CRC{ whole payload }(I) ]| 7       | NO - NO - NO- NO |
|delete event        | deletes event    |[  msg_id(H) msg_type=**17** (B) event_id(H) ]   |    5      |[ msg_id(H) msg_type=**17** (B) event_id(H) ]| 5       | NO - NO - NO- NO |
|error response        | error while processing request | *whichever request*  |    *n*       |[ msg_id(H) msg_type= **0** (B) error(B) ]| 4       | OK -OK-OK-OK |

**Notes:** 
1. I am not sure we need 2 bytes for storing the strategy/event id, I think 1 byte is enough.

3. Possible errors, described in the next section

4. Description of some commands:
    1.  *Ask for node version* Should return a message payload that contains he *version* parameter. This parameter *version* has 8 bytes, the first 4 bytes correspond to the version of the stack: *MAJOR.MINOR.REVISION.BUILDNUMBER*. The next 4 bytes correspond to the *MAJOR.MINOR.REVISION.BUILDNUMBER* for the app that we installed into the node.
    2.  **weekly** refers if the event is repeted weekly, or daily. If *weekly* is *False* the event repeats daily, if weekkly is *True* we should specify which days of the week the event repeats.


5. Doubts about our design:
   1. If node is already on, can a cloud send another led on command? Does the cloud have to check the database first? Does the gateway have to send it to the node anyway and then give an error message to the cloud?
   2. Who is gonna connect to the cloud? all the lamp posts in the world?
   3. How many lamp posts does Salvi have in the world? According to > https://cities-today.com/a-quarter-of-streetlights-could-be-smart-by-2030/ there will be around 361 million street light in the world. At most 622 million if we add tunnel lights, and stadium lights.
   4. How are we going to choose the msg id? do we identify it with the node? If so, do we keep track of the last message id sent, per node? or not? I can think of 3 ways of doing it:
      1. Choose a message id of 8 bytes, and update it in general -> makes the message heavier
      2. Choose a message id of 2 bytes, and update it for each node separately -> a lot of database and CPU consumption
      3. Invent a random message id of 2 bytes, and update it in general -> the probabilities that the same node will repeat the message id are 2.3*10^-10 (0.00000000002) so it will need to send 65000 messages before it can be repeated.
      4. **make front end block** new messages to the same nnode, until the response is received.

6. The gateway answers to this cloud request by publishing the response on topic `gw-res/n/<node_id>`
7. Message examples:

- Cloud tells node 145 to open the led: The Cloud will publish on topic `cl-req/n/145` the following message: 
`500 1` (this message contains the message id "500" and the type of order/message which is also 1). Once the message is received and processed by the gateway, the gateway will send it to the node and publish a response to this call, at topic `gw-res/n/145` with the message `500 1` (same message id so that the caller can identify the response in the topic).
- Cloud tells node 145 to turn off the led: The Cloud will publish topic `cl-req/n/145` the following message:: 
`501 2` (this message contains the message id "501" and the type of order/message which is 2). If the gateway receives the message it will publish a response on topic `gw-res/n/145` with message payload: `501 2`.
- Cloud tells node 145 to set a dimming of 66%: The Cloud will publish topic `cl-req/n/145` the following message:: 
`502 3 66` (this message contains the message id "502" and the type of order/message which is 3, and includes the dimming of 66%). The response will be published at topic `gw-res/n/145` with message payload: `502 3 66`.
- Cloud tells node 145 to set a dimming of 20%: The Cloud will publish topic `cl-req/n/145` the following message:: 
`503 3 20` (this message contains the message id "503" and the type of order/message which is 3, and includes the dimming of 20%). Now the node encounters an error in which it can't detect the driver and then it gives a response that will be published at topic `gw-res/n/145` with message payload: `503 0 1`.


#### Cloud to gateway messages

The process for this kind of messages is the following:

1. The cloud will send this message to the gateway
2. The gateway will take it, process it and issue a response to the cloud.

**Note**: We don't forward the message to the *nodes* in this kind of messages. 

|message name   | description   | Call  | bytes  | response  |  bytes  | cl-gw-test | 
|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|:-----------------:|:-----------------:|
|node list     | get nodes connected to gateway  |[  msg_id(H) msg_type= **4** (B) client_id(I) ]    |    7          |[  msg_id(H) msg_type= **4** (B) client_id(I) num_nodes(H) node_ids(Q)*num_nodes]      | 9 + 8·num_nodes           | NO - OK (asks sink OR invents them) - NO |
|remove nodes     | remove nodes from gw database   |[ msg_id(H) msg_type= **6** (B)  num_nodes(H) node_ids(Q)*num_nodes ] |    5  + 8·num_nodes        |[ msg_id(H) msg_type= **6** (B)   CRC{ num_nodes node_ids) }(I)  ]    | 7           | NO - OK (but gw invents them)- NO |
|update gateway*     |  update gateway software from github  *takes around 30sec to complete* | [ msg_id(H) msg_type= **7** (B) ] |    3        |[ msg_id(H) msg_type= **7** (B)    ]    | 3            |  NO - OK - NO |
|update nodes*     |  update nodes using OTAP |  [ msg_id(H) msg_type= **8** (B) ] |    3        |[ msg_id(H) msg_type= **8** (B)    ]    | 3              | NO - OK - NO |
|get gw version*     |  get the gateway version |  [ msg_id(H) msg_type= **9** (B) ] |    3        |[ msg_id(H) msg_type= **9** (B) version(BBBB)    ]    | 7            |   NO - NO - NO |
|error response        | error while processing request     | *whichever request*  |    *n*       |[ msg_id(H) msg_type= **0** (B)  error(B) ]| 4         | OK - OK - OK |


**Notes**
1. The *node list* message has been simulated from cloud-gateway with a maximum ammount of nodes of 13561 (108500 bytes)  
2. On *node list* a *client_id=0* means give me the nodes of all clients connected to this gateway.


#### Gateway to cloud messages

The process for this kind of messages is the following:

1. The gateway  will send this message to the cloud
2. The cloud will take it, process it and issue a response to the gateway.

|message name   | description   |   Call |  bytes  | response  | bytes  | cl-gw-test | 
|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|:-----------------:|
|alive          | echo signal to send ID to mqtt topic `gw-req/gw-init/<gw-id>`  |[ msg_id(H) msg_type= **1** (B) gw_ip1(B) gw_ip2(B) gw_ip3(B) gw_ip4(B) ]     |   11         |[ msg_id(H) msg_type= **1** (B) gw_ip1(B) gw_ip2(B) gw_ip3(B) gw_ip4(B)]       |  11               | NO - NO - NO |
|disconnect          | echo signal to send ID to mqtt topic `gw-disconnect/<gw-id>` | [ gw_id(Q) ]     |   8         |[ gw_id(Q) ]       |  8               | NO - OK - NO |
|add nodes       | tells which nodes have been added to this gateway recently   |[ msg_id(H) msg_type= **2** (B)  num_nodes(H) node_ids(Q)*num_nodes ] |    5  + 8·num_nodes        |[ msg_id(H) msg_type= **2** (B)   CRC{ num_nodes node_ids }(I)  ]    | 7            | OK - OK - YES (gw fakes nodes, cloud fakes crc) | 
| not seen nodes       | tells which nodes aren't seen anymore in this gateway recently     |[ msg_id(H) msg_type= **3** (B)  num_nodes(H) node_ids(Q)*num_nodes ] |    5  + 8·num_nodes          | [ msg_id(H) msg_type= **3** (B)   CRC{ num_nodes node_ids }(I)  ]    | 7           | OK - OK - YES (gw fakes nodes, cloud fakes crc) |    
|node status list     | sends status of the selected nodes    | [  msg_id(H) msg_type= **4** (B) num_nodes(H) { node_ids(Q) led_state(B) dimming(b) num_neighb(I) rssi(b) hops(B) }*num_nodes]        | 5 + 16·num_nodes     |[ msg_id(H) msg_type= **4** (B)   CRC{ all arguments }(I)  ]    |  7          | OK - OK - YES (gw fakes nodes, cloud fakes crc) |
|alarm       | sends alarm to cloud concerning several nodes | [ msg_id(H) msg_type= **5** (B)  alarm_type(B) num_nodes(H) node_ids(Q)*num_nodes ] |    6+8·num_nodes  |[ msg_id(H) msg_type= **5** (B)  alarm_type(B) CRC {all arguments(I) }  ]    | 8            | OK - OK - YES (gw fakes alarm & nodes, cloud fakes crc) |
|electric parameters list       | sends consumptions to cloud    | [ msg_id(H) msg_type= **6** (B)   num_nodes(H) { node_ids(Q) voltage(H) current(H) power(H) frequency(B) light_level(B) running_hours(I)}*num_nodes ] |   5 + 20·num_nodes  |[ msg_id(H) msg_type= **6** (B)   CRC{ all arguments }(I) ]    | 7            | OK - OK - YES (gw fakes parameters, cloud fakes crc) |
|error response        | error while processing request    | *whichever request*  |    *n*       |[ msg_id(H) msg_type= **0** (B)  error(B) ]| 4      | NO - NO - NO |


### Possible errors
  1. **Driver doesn't respond** The request was processed from gateway to node, but the driver seems to not operate as expected.
  2. **Node doesn't respond** The gateway can't establish a connection with the desired node.
  3. **Node has ROM full** The node receives the message but can't store more information into its static memory.
  4. **Gateway has ROM full** The gateway can't store the required information in its static memory.
  5. **Gateway error while connecting to local database** The gateway tried to connect to the database but couldn't.
  6. **incorrect message length** The gateway tried to connect to the database but couldn't.
  7. **parameters out of range** Some of the parameters sent are not in the expected range of values. i.e. when a dimming of 129% is sent. Dimming should be between 0 and 100.
  8. **node not in gateway** There is a node not in the gateway that the cloud wanted the gateway to modify
  9. **invalid CRC** The CRC received on the response doesn't match the original message sent from the gateway
  10. **Strategy not found** The strategy sent is not in the gateway database
  11. **error while updating gateway database**
  12. **error while reading gateway database** The database could not be read
  13. **error while updating gateway software** The Gateway tried to update, but the operation wasn't successful
  14. **error in tunneling cloud > node** The tunneling step after receiving the cloud message, didn't go as expected
  15. **Invalid message type** The message type sent is not recognized
  16. **Message payload not in bytes** The message payload received is not in bytes. It should be in bytes to be processed properly
  17. **Invalid message origin (mqtt topic)** The MQTT topic is wrong or not the expected one.
  18. **Couldn't update nodes (OTAP)** The OTAP request sent to the gateway, didn't go as expected


# How to use the gateway backend API

## Taking remote control of the gateway

Each gateway runs a python script called `remote_control_gw.py` at the start of the gateway services, which makes the gateway connect to the global broker in these two MQTT topics:

1. `cl-req/remote-gw/<gw_id>` as a subscriptor
2. `gw-res/remote-gw/<gw_id>` as a publisher

This enables the gateway to receive shell commands from the cloud, execute them during its runtime, and return the output of the execution.

In order to control a gateway remotely and send a command to it, and see the output, run the script: 

```
remote_control_cloud.py
```

<!-- I followed this guide > https://gcore.com/support/articles/4408223538321/ -->

## Gateway details

### List of gateways ever connected to the local broker

This can be consulted by running the following default wirepas script and command:

```
cd otap; cd examples; python3 example_list_sinks.py --host 127.0.0.1 --port 1883 --username roma_masana --password all_I_want_for_christmas_is_you --insecure
```





## Changing the sink configuration

You can change the sink configuration using the gateway backend API. You have to run the script called `otap_menu.py` and then choose the mode **10** for *Set a new sink configuration*. IN this mode you will be asked the:

1. Current sink network address
2. The new sink network address
3. The new sink network channel
4. If you want to start the sink stack after the configuration is done

**Note**: If the sink stack was *inactive* and you activate it using this script, it will take about 5 minutes until the sink is fully operational and can detect and communicate with the nodes around her.

There are a few quick commands that allow you to **control the sink configuration**. If you run the previous script, you can:

1. Activate all sinks within Gateway's reach
2. Upload a scratchpad to all the sinks
3. Process a scratchpad on all the sinks
4. Change the sink time delay's for propagate and process
5. You can set the sink to no OTAP
6. You can make the sink go OTAP to the nodes.

Furthermore, you can **extract the following information** from the sink, running the previous script:

1. Display the sink status, and the scratchpad of all the nodes connected to it
2. List all sink names and their gateway id
3. Get the stack and app node versions
4. Get the list of nodes the gateway can reach

# How does the gateway's backend API code work?

The code we developped here is based on the following documentation of Wirepas:

1. Guide on how to communicate with a wirepas network using the wirepas Gateway API > https://developer.wirepas.com/support/solutions/articles/77000487992-how-to-communicate-with-a-wirepas-network-using-wirepas-gateway-api
2. Wirepas Mesh concepts > https://developer.wirepas.com/support/solutions/articles/77000484367-wirepas-mesh-concepts
3. Wirepas mqtt library > https://github.com/wirepas/wirepas-mqtt-library
4. Backend APIs, gateway to backend: https://github.com/wirepas/backend-apis/tree/master/gateway_to_backend#api-between-a-gateway-and-wirepas-backends
5. Wirepas mesh messagin in python > https://github.com/wirepas/wirepas-mesh-messaging-python

## Notes

1. Wirepas recommends *As described in the beginning of this chapter, it is recommended to publish this event with a QoS1 to avoid loading too much the broker.*

## How is the Gateway's id number chosen?

You can either assign it by hand, or let the wirepas software assign it automatically.

If you assign it by hand you have to control that each gateway has a *unique id*. 

You can let wirepas software determine it automatically. How does wirepas assign a unique id to each device? It is not published and it is kept secrete as intellectual property of wirepas.


# Connectivity tests

## 1. Barcelona lab

**Notes**

1. Node num of neighbours doesn't update if I turn off a node from the mesh network. Even after some minutes the *number of neighbours* from the other nodes reports the same number. This should change.

2. Every cloud  > node message, seems to take 500 - 1.000 B of download and upload for the gateway. Considering that the payload of each of these messages is around 1-20 B, this doesn't make much sense. The issue should be investigated since the real size is 50 x bigger than the size of the payload.
    - Why is that? we have to investigate this issue

      1. he entrat al servidor cloud, i cada comanda posa que envia 20B com a molt, com pot ser llavors?
      2. he posat qos=0, i molts missatges no arriben, i cada un segueix costant 0.5KB, per tant ho mantenim en qos=1


3. The python code errors, when calling `create_wni()` or `wni.list_sinks()` or `wni.list_gateways()` defined in the wirepas python script called `wirepas_network_interface.py` may originate, as explaind by wirepas code comments themselves, because of a:
     - An offline gateway that will never be back online (removed from network)
     - A sticky gateway online status that is not here anymore (bug from gateway)
     - A malformed gateway status (bug from gateway)
In order to clear this problem, it is suggested that you run the following wirepas function in the code, to clear that malformed gateway id: `wni.clear_gateway_status(gw_id)`.
- Update on this, after running 2 times the code with the  `clear_gateway_status(gw_id)` right after creating the "WNI", I managed to get rid of this error.


## 2. Dammam

**Notes**

1. We observe that when the front-end or cloud tells node 280 to open, it takes sometimes up to **15 seconds** for the `cl-req` to recieve its `gw-resp` (response). Hypotheses of what might be happening
   1. If the gateway had perfect internet connection, and the delay was due to the gateway-node connection, then the gateway would anser after 7 seconds (the gateway-node timeout is set to 7 seconds) that no response is received, to the clouod. It would report a *type 0* message with *type 2* error, as we have seen many times when the node doesn't answer in time.
   2. Therefore the only plausible explanation is the lack of internet connectivity. This would make the gateway receive the cloud message with a delay, and also have a delay when sending backe the response. 
   3. The total amount of more than 15 seconds observed has at least 7 seconds attributable to the internet connection

2. We also observed sometimes the cloud message having a response and the lamp turning off/on in less than 1 second, other times it took 16 seconds.
3. The gateway at dammam downloaded all of a sudden 56MB of data, could it be that the `git fetch/ git reset` forced the gw to download all code even if 90% of the code is identical to the local repo? > https://www.theserverside.com/blog/Coffee-Talk-Java-News-Stories-and-Opinions/Git-pull-vs-fetch-Whats-the-difference

