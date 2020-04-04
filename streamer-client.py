import socket
import getpass

addr = ('127.0.0.1', 9999)
def conn():
    s = socket.socket()
    try:
        #establish connection
        s.connect(addr)
        streamername = input("enter your username:")
        streamerpass = input("enter your password:")
        s.send(f"streamer:{streamername}+{streamerpass}".encode("utf-8"))
        data = s.recv(1024).decode("utf-8")
        print(data)
        if data.startswith("error:"):
            return
        token = data[-16:]
        while True:
            output = input()
            bcount = s.send((token + ":" +output).encode("utf-8"))
            print("send>>>[{}B] ".format(bcount), output)
    except Exception as e:
        print(e)
    finally:
        s.close()

if __name__ == '__main__':
    conn()

