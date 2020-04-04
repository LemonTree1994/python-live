#server
import socket, threading, time
#TCP socket based on ipv4
from concurrent.futures import ThreadPoolExecutor
users = []
lock = threading.Lock()
pool = ThreadPoolExecutor()

def main():
    s = socket.socket()
    # listening on port
    s.bind(('127.0.0.1', 9999))
    s.listen()
    while True:
        # receive a new connect
        sock, addr = s.accept()
        pool.submit(process,sock,addr)

def sendtoall(data):
    global users
    pool.map(senddata,[(sock,data) for sock in users if not getattr(sock,"_closed", True)])

def senddata(args):
    sock, data = args
    sock.send(data)


def process(sock: socket.socket, addr):
    try:
        sock.send(b"Welcome!")
        info = sock.recv(1024).decode("utf-8")
        if info == "streamer":
            while True:
                data = sock.recv(1024)
                if not data:
                    break
                sendtoall(data)
        elif info == "user":
            lock.acquire()
            global users
            users.append(sock)
            lock.release()
    except Exception as err:
        print(err)
        sock.close()


if __name__ == '__main__':
    main()