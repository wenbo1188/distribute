from server_comm import mySerSocket

def main():
    myServer = mySerSocket("59.78.25.163", 5000)
    socket = myServer.createSerSocket()
    myServer.startSerSocket(socket, 5, 1024)
    myServer.destroySerSocket()

if __name__ == '__main__':
    main()
