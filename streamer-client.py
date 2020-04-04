import socket
import time
def conn():
    s = socket.socket()
    try:
        #establish connection
        s.connect(('127.0.0.1', 9999))
        data = s.recv(1024)
        print(data.decode("utf-8"))
        s.send("streamer".encode("utf-8"))
        while not getattr(s,"_closed",True):
            output = input().encode("utf-8")
            s.send(output)
            print("send>>> ", output)
    except Exception as e:
        print(e)
    finally:
        s.close()

if __name__ == '__main__':
    conn()

