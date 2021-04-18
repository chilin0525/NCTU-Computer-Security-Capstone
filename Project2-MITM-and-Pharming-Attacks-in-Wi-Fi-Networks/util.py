class ipMAC:
    def __init__(self, ip, mac):
        this.ip = ip
        this.mac = mac

import os
import re

if __name__ == "__main__":
    # username=0711282&password=xxxxxxx&captcha_code=6135HTTP/1.1 303 See Other
    # https://stackoverflow.com/questions/4664850/how-to-find-all-occurrences-of-a-substring
    for file in os.listdir("logdir/"):
        with open("logdir/" + file, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                if ('username=' in line) and ("password=" in line):
                    a = [m.start() for m in re.finditer("&", line)]
                    b = [m.start() for m in re.finditer("=", line)]
                    print(a,b)
                    print(line[b[0]+1:a[0]],line[b[1]+1:a[1]])
                    break

                
