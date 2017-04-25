from socket import *
import struct
import argparse
import time

def main():
    parser = argparse.ArgumentParser(description="tcp receiver parser")
    parser.add_argument('ip',help="set up sender ip")
    parser.add_argument('port',help="set up sender port",type=int)
    args = parser.parse_args()
    ADDR = (args.ip, args.port)
    BUFSIZE = 1024
    FILEINFO_SIZE=struct.calcsize('128s32sI8s')
    recvSock = socket(AF_INET,SOCK_STREAM)
    recvSock.bind(ADDR)
    recvSock.listen(True)
    print("waiting for connection...")
    conn,addr = recvSock.accept()

    # timer set up
    time1 = time.time()
    print "connection established -> ",addr
    fhead = conn.recv(FILEINFO_SIZE)
    filename,temp1,filesize,temp2=struct.unpack('128s32sI8s',fhead)
    print("filename:%s,filename length:%s,file type:%s" %(filename, len(filename), type(filename)))
    print("filesize:%s" % filesize)
    filename = 'new_'+filename.strip('\00')
    fp = open(filename,'wb')
    restsize = filesize
    print("receiving files...")
    while 1:
        if restsize > BUFSIZE:
            filedata = conn.recv(BUFSIZE)
        else:
            filedata = conn.recv(restsize)
        if not filedata: break
        fp.write(filedata)
        restsize = restsize-len(filedata)
        if restsize == 0:
            break
    print("file transfer finished, releasing connection...")
    fp.close()
    conn.close()
    recvSock.close()
    time2 = time.time()
    print("connection released!")
    print("time consumed is %f" %(time2-time1))

if __name__ == '__main__':
    main()
