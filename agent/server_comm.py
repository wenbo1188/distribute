import socket

class mySerSocket:
    def __init__(self, ip, port, socket=None):
        self.ip = ip
        self.port = port
        self.socket = socket
        
    def createSerSocket(self):
        self.socket = socket.socket()
        self.socket.bind((self.ip, self.port))
        return self.socket

    def destroySerSocket(self):
        self.socket.close()

    def startSerSocket(self, socket, listen_num=5, buffer_size=1024):
        if socket != None:
            socket.listen(listen_num)
            flag = True
            while flag:
                clisock, cliaddr = socket.accept()
                
                data = clisock.recv(buffer_size)
                print("from client:"+cliaddr+" "+data)
                if data == 'exit':
                    flag = False
                clisock.send("OK!")
            clisock.close()
        else:
            print("Socket Error!\n")

class myCliSocket:
    def __init__(self, ip, port, socket=None):
        self.ip = ip
        self.port = port
        self.socket = socket

    def createCliSocket(self):
        self.socket = socket.socket()
        return self.socket

    def destroyCliSocket(self):
        self.socket.close()

    def startCliSocket(self, socket, buffer_size, send_content=None):
        if send_content == None:
            if socket != None:
                socket.connect((self.ip, self.port))
                inform = raw_input('client>')
                socket.send(inform)
                response = socket.recv(buffer_size)
                print("get info:"+response)
                return response
            else:
                print("Socket Error!\n")
                return None
        else:
            if socket != None:
                socket.connect((self.ip, self.port))
                socket.send(send_content)
                response = socket.recv(buffer_size)
                print("get info:"+response)
                return response
            else:
                print("Socket Error!\n")
                return None


    
        



