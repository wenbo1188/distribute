from server_comm import myCliSocket
import json

data = {"type":"REQUEST","inform":{"problem":"7"}}

data_string = json.dumps(data)

def main():
    myClient = myCliSocket("10.42.0.1", 5050)
    socket = myClient.createCliSocket()
    myClient.startCliSocket(socket, 1024, data_string)
    myClient.destroyCliSocket()

if __name__ == '__main__':
    main()


