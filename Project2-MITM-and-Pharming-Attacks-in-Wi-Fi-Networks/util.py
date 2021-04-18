class ipMAC:
    def __init__(self, ip, mac):
        this.ip = ip
        this.mac = mac

import os
for file in os.listdir("logdir/"):
    with open("logdir/" + file, 'r', encoding='utf-8',
              errors='ignore') as f:
        for line in f:
            if ('username=' in line) and ("password=" in line):
                print("Find: ",line)
                
