from pwn import *

# connect socket with remote server
r = remote('140.113.207.240', 8831)

r.recvline()
r.sendline('-559038801')  
r.recvline()
r.sendline('YOUSHALLNOTPASS')
# r.interactive()
print(r.recv())
print(r.recv())
r.close()
