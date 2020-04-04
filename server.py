#server
import socket, threading, time
#TCP socket based on ipv4
from concurrent.futures import ThreadPoolExecutor
users = []
lock = threading.Lock()
pool = ThreadPoolExecutor()
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind(('127.0.0.1', 9999))

def main():
    while True:
        data, addr = s.recvfrom(1024)
        print("from {} >>> {}".format(addr,data.decode("utf-8")))
        data = data.decode("utf-8")
        if data.startswith("streamer:"):
            pool.submit(sendtoall,data[9:].encode("utf-8"))
        else:
            s.sendto(b"Welcome!", addr)
            if data== "user":
                lock.acquire()
                global users
                users.append(addr)
                lock.release()

def sendtoall(data):
    global users
    pool.map(senddata,[(data, addr) for addr in users])

def senddata(args):
    data, addr = args

    print("sending {} to {}".format(data,addr))
    s.sendto(data,addr)

if __name__ == '__main__':
    main()