#server

import socket, threading
import string
import random
from concurrent.futures import ThreadPoolExecutor

# database
streamers = {
    "li": "1234"
}
token_string = string.ascii_letters+string.digits

# online
# onlinestreamersubers :{"streamer name": [online user list]}
onlinestreamersubers = {}
# onlinestreamers: {token : streamer name}
onlinestreamers = {}

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
    print(data)
    if data.startswith("streamer:"):
        streamername, streamerpass = data[9:].split("+")
        print(streamername, streamerpass)
        if not isexitstreamer(streamername, streamerpass):
            sock.send("error: wrong auth".encode("utf-8"))
            return
        token = "".join(random.sample(token_string,16))
        onlinestreamers[token] = streamername
        print(onlinestreamers)
        pool.submit(sendtoall, streamername, f"streamer {streamername} online".encode("utf-8"))
        sock.send(f"Welcome, streamer: {streamername},your token is {token}".encode("utf-8"))
    else:
        sock.send("error: wrong input".encode("utf-8"))
        return
    while True:
        data = sock.recv(1024).decode("utf-8")
        print(data)
        if not data:
            break
        token = data[:16]
        data = data[17:]
        print(token,data)
        streamername = onlinestreamers.get(token)
        if streamername is None:
            sock.send("error: token error".encode("utf-8"))
            return
        pool.submit(sendtoall, streamername, data.encode("utf-8"))

def isexitstreamer(username,password):
    streamerpass = streamers.get(username)
    if streamerpass is None or streamerpass != password:
        return False
    return True


def sendtoall(streamername, data):
    print("sendtoall")
    for addr in onlinestreamersubers.get(streamername,[]):
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
        subers = onlinestreamersubers.get(streamername, [])
        if len(subers) ==0:
            onlinestreamersubers[streamername] = subers
        subers.append(addr)
        lock.release()
        print(onlinestreamersubers)
        sudp.sendto(f"You are the {len(subers)}th user who subscribed streamer {streamername}".encode("utf-8"), addr)

    else:
        sudp.sendto("error", addr)


if __name__ == '__main__':
    main()