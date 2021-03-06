from server_comm import mySerSocket
from server_comm import myCliSocket
import sqlite3 as sqlite
import json

class manageServer:
    '''
    def __init__(self, dbname, socket):
        self.con = sqlite.connect(dbname)
        self.socket = socket

    def __del__(self):
        self.con.close()
        self.socket.close()

    def updatepeople(self, from_ip, message):
        self.con.execute("update people set address='%s', skills='%s', serverip='%s' where name='%s'" \
                % (message["address"], message["skills"], from_ip, message["name"]))
        print("people updated\n")
        self.con.commit()

    def addpeople(self, from_ip, message):
        self.con.execute("insert into people values(?, ?, ?, ?)", (message["name"], message["address"],\
                message["skills"], from_ip))
        print("people added\n")
        self.con.commit()

    def delpeople(self, name):
        self.con.execute("delete from people where name='%s'" % name)
        print("people deleted\n")
        self.con.commit()
    
    def dealmessage(self, from_ip, message):
        if message["type"] == "REQUEST":
            self.dealrequest(from_ip, message["inform"]["problem"])
        elif message["type"] == "UPDATE":
            self.updatepeople(from_ip, message["inform"])
        elif message["type"] == "ADD":
            self.addpeople(from_ip, message["inform"])
        elif message["type"] == "DEL":
            self.delpeople(message["inform"]["name"])
        else:
            print("Error message!\n")

    def dealrequest(self, from_ip, problem_num):
        cur = self.con.execute("select serverip from people where skills='%s'" % problem_num)
        res = cur.fetchone()
        if res == None:
            self.requestother(from_ip, problem_num) 
        else:
            print "problem distributed to %s\n" % res
            
    def requestother(self, from_ip, problem_num):
        print "request other manage server\n"

    def createdb(self):
        self.con.execute('drop table if exists people')
        self.con.execute('create table people(name, address, skills, serverip)')
        self.con.commit()
    
    def startServer(self, listen_num=5, buffer_size=1024):
        if self.socket != None:
            self.socket.listen(listen_num)
            flag = True
            while flag:
                clisock, cliaddr = self.socket.accept()
                message = clisock.recv(buffer_size)
                # print type(cliaddr)
                # print type(message)
                print "from IP:%s PORT:%s message:%s" % (cliaddr[0], cliaddr[1], message)
                tuple_message = json.loads(message) 
                self.dealmessage(cliaddr[0], tuple_message)
                if message == "exit":
                    flag = False

                clisock.send("200 OK!")
            clisock.close()
        else:
            print("Socket Is Null!\n")
    '''
    def __init__(self, file, socket, localIp=None):
        self.file = file
        self.socket = socket
        if localIp == None:
            self.localIp = []
            for line in self.file:
                if line != "\n":
                    self.localIp.append(line[:-1])
        else:
            self.localIp = localIp

    def __del__(self):
        self.socket.close()
        self.file.seek(0,0)
        for ip in self.localIp:
            self.file.write(ip + "\n")
        self.file.close()
    
    def dealmessage(self, from_ip, message, socket):
        if message["type"] == "HI":
            try:
                self.localIp.append(from_ip)
                print("ip %s was added!\n" % from_ip)
            except:
                print("Still exist ip %s\n" % from_ip)
            self.localIp = list(set(self.localIp))
            socket.send("200 OK!")
        if message["type"] == "BYE":
            try:
                self.localIp.remove(from_ip)
                print("ip %s was deleted!\n" % from_ip)
            except:
                print("Do not have ip %s\n" % from_ip)
            self.localIp = list(set(self.localIp))
            socket.send("200 OK!")
        if message["type"] == "FIND":
            stringData = json.dumps(self.localIp)
            for item in self.localIp:
                print("%s\n" % item)
            socket.send(stringData)
            
    def startServer(self, listen_num=5, buffer_size=1024):
        if self.socket != None:
            self.socket.listen(listen_num)
            flag = True
            while flag:
                clisock, cliaddr = self.socket.accept()
                message = clisock.recv(buffer_size)
                tuple_message = json.loads(message)
                self.dealmessage(cliaddr[0], tuple_message, clisock)
                if message == "exit":
                    flag = False
            clisock.close()
        else:
            print("Socket Is Null!\n")

def main():
    '''
    ip = '59.78.25.163'
    port = 5050
    myserversocket = mySerSocket(ip, port)
    socket = myserversocket.createSerSocket()
    manager = manageServer('manage.db', socket)
    manager.createdb()
    manager.startServer()
    '''
    ip = '59.78.25.163'
    port = 5050
    myserversocket = mySerSocket(ip, port)
    socket = myserversocket.createSerSocket()
    
    f = open("localip.txt","r+")
    if f == None:
        print("file open failure!\n")
    else:
        manager = manageServer(f, socket)
        manager.startServer()

if __name__ == '__main__':
    main()  
