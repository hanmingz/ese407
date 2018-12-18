# Mininet Project

ESE 407 Final Project A (Homework 3).<br/>
Team members: Hanming Zu, Han Yan

## Environment Setup

For this project, we use Mininet VM.
After starting the VM, login with username: mininet and password: mininet.
<br/>
### Source files:
project.py<br/>
rip.py

To bring up wireshark and run the python script:

```bash
startx 
cd mininet/ese407
sudo python project.py
```

## Detailed Explanation

![alt text](https://s3.amazonaws.com/pwcs2018/topology.png)
This topology is consisted of 6 hosts, 2 switches and 4 routers, with links shown in the diagram. To experiment with 'traceroute', we need multiple routers and multiple potential paths between hosts in order to utilize TTL and 'time_exceeded' responses.
<br/>
project.py installs all the software needed, starts wireshark in the background and generates the topology and routing tables by calling functions in rip.py.<br/>
To capture packets in Wireshark after running project.py, simply type in the commands specified in Homework 3 in the terminal and use 'of' filter to look up only the openflow packets.
