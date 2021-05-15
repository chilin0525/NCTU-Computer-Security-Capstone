class ssh_data():
    
    username = ""
    passwd   = ""
    port     = 22
    
    def __init__(self,username,passwd,port=22):
        self.username = username
        self.passwd   = passwd
        self.port     = port