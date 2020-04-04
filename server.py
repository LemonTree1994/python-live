#server
import socket, threading, time
#TCP socket based on ipv4
from concurrent.futures import ThreadPoolExecutor

streamersubers = dict()
streamers = dict()

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
        pool.submit(processstreamersocket, sock)

def processstreamersocket(sock):
    print("enter processstreamersocket")
    data = sock.recv(1024).decode("utf-8")
    if data.startswith("streamer:"):
        streamername = data[9:]
        if streamername in streamers.keys():
            sock.send(f"error: streamer name {streamername} repeat".encode("utf-8"))
            return

        streamers[streamername] = sock
        print(streamers)
        pool.submit(sendtoall, streamername, f"streamer {streamername} online".encode("utf-8"))
        sock.send(f"Welcome, streamer: {streamername}".encode("utf-8"))
    else:
        sock.send("error: no streamer name".encode("utf-8"))
        return
    while True:
        data = sock.recv(1024)
        if not data:
            break
        pool.submit(sendtoall, streamername, data)


def sendtoall(streamername, data):
    print("sendtoall")
    for addr in streamersubers.get(streamername,[]):
        pool.submit(senddata, data, addr)

def senddata(data, addr):
    print("send data")
    sudp.sendto(data, addr)


def recv_user():
    try:
        while True:
            # receive a new message
            data, addr = sudp.recvfrom(1024)
            print("user connected")
            pool.submit(processuser, data,addr)
    except Exception as e:
        print(e)

def processuser(data, addr):
    print("enter processuser")
    data = data.decode("utf-8")
    if data.startswith("sub:"):
        streamername = data[4:]
        lock.acquire()
        subers = streamersubers.get(streamername, [])
        if len(subers) ==0:
            streamersubers[streamername] = subers
        subers.append(addr)
        lock.release()
        print(streamersubers)
        sudp.sendto(f"You are the {len(subers)}th user who subscribed streamer {streamername}".encode("utf-8"), addr)

    else:
        sudp.sendto("error", addr)
if __name__ == '__main__':
    main()