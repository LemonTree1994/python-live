#server
import socket, threading, time
#TCP socket based on ipv4
from concurrent.futures import ThreadPoolExecutor
users = []
lock = threading.Lock()
pool = ThreadPoolExecutor()


tcp_addr = ("127.0.0.1", 9999)
udp_addr = ("127.0.0.1", 8888)

sudp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sudp.bind(udp_addr)

stcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
stcp.bind(tcp_addr)
stcp.listen()

def main():

    # pool.submit(recv_streamer)
    # pool.submit(recv_user)
    # 使用线程池出现问题，Break a reference cycle with the exception 'exc'

    th1 = threading.Thread(target=recv_streamer)
    th1.start()
    th2 = threading.Thread(target=recv_user)
    th2.start()

def recv_streamer():
    while True:
        sock, addr = stcp.accept()
        print("streamer connected")
        sock.send(b"Welcome, streamer")
        pool.submit(processstreamersocket, sock)

def processstreamersocket(sock):
    print("enter processstreamersocket")
    while True:
        data = sock.recv(1024)
        if not data:
            break
        pool.submit(sendtoall, data)
        print("submit sendtoall")

def sendtoall(data):
    global users
    for addr in users:
        pool.submit(senddata, data, addr)

def senddata(data, addr):
    sudp.sendto(data, addr)
    print("send data")


def recv_user():
    try:
        while True:
            # receive a new message
            data, addr = sudp.recvfrom(1024)
            if data.decode("utf-8")=="user":
                lock.acquire()
                global users
                users.append(addr)
                lock.release()
                print(users)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()