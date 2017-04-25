from socket import *
import os
import struct
import argparse


def main():
    parser = argparse.ArgumentParser(description="tcpsender parser")
    parser.add_argument('ip', help="set up sender ip")
    parser.add_argument('port', help="set up sender port", type=int)
    parser.add_argument('filename', help="select a filename")
    args = parser.parse_args()
    ADDR = (args.ip, args.port)
    BUFSIZE = 1024
    filename = args.filename
    FILEINFO_SIZE=struct.calcsize('128s32sI8s')
    sendSock = socket(AF_INET,SOCK_STREAM)
    sendSock.connect(ADDR)
    fhead=struct.pack('128s11I',filename,0,0,0,0,0,0,0,0,os.stat(filename).st_size,0,0)
    sendSock.send(fhead)
    fp = open(filename,'rb')
    while 1:
        filedata = fp.read(BUFSIZE)
        if not filedata: break
        sendSock.send(filedata)
    print("file transfer finished!")
    fp.close()
    sendSock.close()
    print("connection released!")

if __name__ == '__main__':
    main()
