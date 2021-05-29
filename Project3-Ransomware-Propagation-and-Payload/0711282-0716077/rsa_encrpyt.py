import sys
import pickle

n = int(22291846172619859445381409012451)
e = int(65535)
filename = sys.argv[1]

plain_bytes = b''
with open(filename, 'rb') as f:
    plain_bytes = f.read()
cipher_int = [pow(i, e, n) for i in plain_bytes]
with open(filename, 'wb') as f:
    pickle.dump(cipher_int, f)
