import socket
import threading
import time

def main():
    s = socket.socket()

    try:
        #establish connection
        s.connect(('127.0.0.1', 9999))
        data = s.recv(1024)
        print(data.decode("utf-8"))
        s.send("user".encode("utf-8"))
        print("i am an user, i am looking the live")
        #receive  message
        while not getattr(s,"_closed", True):
            data = s.recv(1024)
            print("recv>>> ", data.decode("utf-8"))
    except Exception as e:
        print(e)
    finally:
        s.close()

if __name__ == '__main__':
    main()
