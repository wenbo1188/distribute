import json
import urllib
import urllib2
import argparse
from server_comm import myCliSocket

class agent:
    def __init__(self, customer_ip, messageContent, local_distribute_ip, remote_distribute_ips):
        self.customer_ip = customer_ip
        self.messageContent = messageContent
        self.local_distribute_ip = local_distribute_ip
        self.remote_distribute_ips = remote_distribute_ips

    def __del__(self):
        pass

    def dealMessage(self):
        message = self.messageContent
        print message
        url = "http://" + self.local_distribute_ip + ":5000/"
        if message["type"] == "REQUEST":
            # do local request
            print("requesting %s" % self.local_distribute_ip)
            requestUrl = url + "distribute/" + message["inform"]["problem"]
            req = urllib2.Request(requestUrl)
            responseData = urllib2.urlopen(req)
            print(self.preTreat(responseData.read()))
            # do remote request
            for url in self.remote_distribute_ips:
                requestUrl = url + "distribute/" + message["inform"]["problem"]
                req = urllib2.Request(requestUrl)
                responseData = urllib2.urlopen(req)
                print(self.preTreat(responseData.read()))

        if message["type"] == "ADD":
            # do add
            addUrl = url + "add_user"
            data =  {"name":message["inform"]["name"],"address":message["inform"]["address"], "skills":message["inform"]["skills"]}
            data_encode = urllib.urlencode(data)
            req = urllib2.Request(url = addUrl, data = data_encode)
            responseData = urllib2.urlopen(req)
            print(self.preTreat(responseData.read()))
        if message["type"] == "DEL":
            # do delete
            delUrl = url + "del_user"
            data = {"name":message["inform"]["name"]}
            data_encode = urllib.urlencode(data)
            req = urllib2.Request(url = delUrl, data = data_encode)
            responseData = urllib2.urlopen(req)
            print(self.preTreat(responseData.read()))
        if message["type"] == "UPDATE":
            # do update
            # to be done
            pass

    def preTreat(self, data):
        # to be done
        return data

def getRemoteIp(managerips, localip):
    data = {"type":"FIND"}
    data_string = json.dumps(data)
    remote_distribute_ips = []
    for ip in managerips:
        port = 5050
        myClient = myCliSocket(ip, port)
        socket = myClient.createCliSocket()
        response = myClient.startCliSocket(socket, 1024, data_string)
        if response != None:
            for item in json.loads(response):
                remote_distribute_ips.append(item)
        myClient.destroyCliSocket()

    remote_distribute_ips.remove(localip)
    print remote_distribute_ips
    return remote_distribute_ips

def main():
    managerips = ["59.78.25.163"]
    parser = argparse.ArgumentParser(description='parser for agent')
    parser.add_argument('--type', help='respresent the message type')
    parser.add_argument('--problem', help='represent the problem number')
    parser.add_argument('--customerip', help='represent the customer ip')
    parser.add_argument('--distributeip', help='represent ip of the distribute app')
    parser.add_argument('--name', help='represent name part of the message')
    parser.add_argument('--address', help='represent address part of the message')
    parser.add_argument('--skills', help='represent skills part of the message')
    
    args = parser.parse_args()
    if args.type == "REQUEST":
        message = {"type":"REQUEST", "inform":{"problem":args.problem}}
        myAgent = agent(args.customerip, message, args.distributeip, getRemoteIp(managerips, args.distributeip))
        print("this is a REQUEST message\n")
        myAgent.dealMessage()
    if args.type == "ADD":
        message ={"type":"ADD","inform":{"name":args.name, "address":args.address, "skills":args.skills}}
        myAgent = agent(args.customerip, message, args.distributeip, getRemoteIp(managerips, args.distributeip))
        print("this is a ADD message\n")
        myAgent.dealMessage()
    if args.type == "DEL":
        message ={"type":"DEL","inform":{"name":args.name}}
        myAgent = agent(args.customerip, message, args.distributeip, getRemoteIp(managerips, args.distributeip))
        print("this is a DEL message\n")
        myAgent.dealMessage()
    if args.type == "UPDATE":
        message ={"type":"UPDATE","inform":{"name":args.name, "address":args.address, "skills":args.skills}}
        myAgent = agent(args.customerip, message, args.distributeip, getRemoteIp(managerips, args.distributeip))
        print("this is a UPDATE message\n")
        myAgent.dealMessage()

if __name__ == '__main__':
    main()

