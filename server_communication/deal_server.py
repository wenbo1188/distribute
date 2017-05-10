from server_comm import mySerSocket
from server_comm import myCliSocket
import json
import commands
import argparse

class dealServer:
    def __init__(self, socket, ip, imageName, managerip, numOfContainer=0):
        self.socket = socket
        self.ip = ip
        self.numOfContainer = numOfContainer
        self.imageName = imageName # i.e. "wenbo1188/myagent:3.0"
        self.managerip = managerip
        if not self.signUp():
            print("successfully initialise deal server")
            print("serving at ip %s" % self.ip)
        else:
            print("fail to initialise deal server\n")

    def __del__(self):
        self.socket.close()
        self.dealWithUnfinishedContainer()
        if not self.signOut():
           print("successfully destroy deal server\n")
        else:
            print("fail to destroy deal server\n")

    def dealWithUnfinishedContainer(self):
        pass

    def showNum(self):
        return self.numOfContainer

    def signUp(self):
        data = {"type":"HI"}
        data_string = json.dumps(data)
        ip_address = self.managerip
        port = 5050
        mycliserver = myCliSocket(ip_address, port)
        socket = mycliserver.createCliSocket()
        response = mycliserver.startCliSocket(socket, 1024, data_string)
        mycliserver.destroyCliSocket()
        if response != None:
            print response
            return 0
        else:
            print("sign up failure\n")
            return 1
    
    def signOut(self):
        data = {"type":"BYE"}
        data_string = json.dumps(data)
        ip_address = self.managerip
        port = 5050
        mycliserver = myCliSocket(ip_address, port)
        socket = mycliserver.createCliSocket()
        response = mycliserver.startCliSocket(socket, 1024, data_string)
        mycliserver.destroyCliSocket()
        if response != None:
            print response
            return 0
        else:
            print("sign out failure\n")
            return 1
        
    def increaseNum(self):
        self.numOfContainer += 1
        return self.numOfContainer

    def dealMessage(self, from_ip, message):
        print("Existing %d container\n" % self.showNum())
        self.createContainer(from_ip, message, self.increaseNum() + 6000)

    def createContainer(self, from_ip, message, port_num):
        message = json.loads(message)
        customerip = from_ip
        distributeip = self.ip
        if message["type"] == "REQUEST":
            problemNum = message["inform"]["problem"]
            environmentVar = "-e 'TYPE=REQUEST' -e 'PROBLEM=" + problemNum + "' " + "-e 'CUSTOMERIP=" + customerip + "' " + \
                    "-e 'DISTRIBUTEIP=" + distributeip + "'"
            # print environmentVar #
        if message["type"] == "ADD":
            name = message["inform"]["name"]
            address = message["inform"]["address"]
            skills = message["inform"]["skills"]
            environmentVar = "-e 'TYPE=ADD' -e 'NAME=" + name + "' " + "-e 'ADDRESS=" + address + "' " + "-e 'SKILLS=" + skills + "' " + \
                    "-e 'CUSTOMERIP=" + customerip + "' " + "-e 'DISTRIBUTEIP=" + distributeip + "'"
        if message["type"] == "DEL":
            name = message["inform"]["name"]
            environmentVar = "-e 'TYPE=DEL' -e 'NAME=" + name + "' " + "-e 'CUSTOMERIP=" + customerip + "' " + \
                    "-e 'DISTRIBUTEIP=" + distributeip + "'"
        if message["type"] == "UPDATE":
            pass # to do next
        # command = "docker run " + environmentVar + " -d " + self.imageName 
        command = "docker run " + environmentVar + " -it " + self.imageName
        status, output = commands.getstatusoutput(command)
        print status
        print output
        # to do next
        # take the output and customerip , to send the result to customer

    def startServer(self, listen_num=5, buffer_size=1024):
        if self.socket != None:
            self.socket.listen(listen_num)
            flag = True
            while flag:
                clisock, cliaddr = self.socket.accept()
                message = clisock.recv(buffer_size)
                self.dealMessage(cliaddr[0], message)
                if message == "exit":
                    flag = False

                clisock.send("200 OK!")
            clisock.close()
        else:
            print("Socket Is Null!\n")

def main():
    parser = argparse.ArgumentParser(description='parser for deal server')
    parser.add_argument('--ip', help='the ip of this node')
    parser.add_argument('--port', type=int, help='the port num of socket this node is using for service support --can\'t use 5050')
    parser.add_argument('--imageName', help='the version of image: i.e. wenbo1188/myagent:#')
    parser.add_argument('--managerip', help='the manager server ip of this node')
    args = parser.parse_args()
    myserversocket = mySerSocket(args.ip, args.port)
    socket = myserversocket.createSerSocket()
    dealer = dealServer(socket, args.ip, args.imageName, args.managerip)
    dealer.startServer()

if __name__ == '__main__':
    main()


