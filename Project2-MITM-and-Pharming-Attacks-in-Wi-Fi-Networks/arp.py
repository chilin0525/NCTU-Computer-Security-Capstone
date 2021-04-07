import os
import subprocess
import socket
import re

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
"""
def nmap(ip):
    tmp = "nmap -sn -n " + ip 
    proc = subprocess.Popen([tmp], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    out2 = out.decode("utf-8")
    return out2

if __name__ == "__main__":
    # get ip
    ip = getHostIp()

    # get all ip of NIC, search ip in NIC
    nic = nicInfo()
    for i in nic:
        # print(ip, " ", i.split("/")[0])
        if(i.split("/")[0]==ip):
            ip = i
            break

    print("Currently Ip address is: "+ip)
    print("--------------------------------------------------")
    print("\n")

    result = nmap(ip)
    print(result)
    print("\n")

    ip = re.findall("\d+\.\d+\.\d+\.\d+", result)
    mac = re.findall(
        "[0-9a-fA-F]{2}[:][0-9a-fA-F]{2}[:][0-9a-fA-F]{2}[:][0-9a-fA-F]{2}[:][0-9a-fA-F]{2}[:][0-9a-fA-F]{2}", result)

    # for i in ip:
    #     print(i)
    # print("--------------------------------------------------")
    
    # for i in mac:
    #     print(i)

    print(ip)