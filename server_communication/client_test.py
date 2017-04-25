from server_comm import myCliSocket
import json

#data = {"type":"HI"}
# data = {"type":"BYE"}
data = {"type":"FIND"}
# data = {"type":"ADD","inform":{"name":"Alice","address":"0101","skills":"6"}}
# data = {"type":"REQUEST","inform":{"problem":"6"}}
# data = {"type":"REQUEST","inform":{"problem":"9"}}
data_string = json.dumps(data)

def main():
    myClient = myCliSocket("59.78.25.163", 5050)
    socket = myClient.createCliSocket()
    myClient.startCliSocket(socket, 1024, data_string)
    myClient.destroyCliSocket()

if __name__ == '__main__':
    main()


