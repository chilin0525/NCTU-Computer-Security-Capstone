import sys
import pickle

n = int(22291846172619859445381409012451)
d = int(14499309299673345844676003563183)

jps_files = glob.glob("*.jpg")

for i in jps_files:
    filename = str(i)
    with open(filename, 'rb') as f:
        cipher_int = pickle.load(f)
        decrypted_int = [pow(i, d, n) for i in cipher_int]
        decrypted_bytes = bytes(decrypted_int)
        
    with open(filename, 'wb') as f:
        f.write(decrypted_bytes)
