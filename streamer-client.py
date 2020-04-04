import socket

addr = ('127.0.0.1', 9999)
def conn():
    s = socket.socket()
    try:
        #establish connection
        s.connect(addr)
        streamername = input("enter your name:")
        s.send(f"streamer:{streamername}".encode("utf-8"))
        data = s.recv(1024).decode("utf-8")
        print(data)
        if data.startswith("error:"):
            return
        while True:
            output = input().encode("utf-8")
            bcount = s.send(output)
            print("send>>>[{}bytes] ".format(bcount), output)
    except Exception as e:
        print(e)
    finally:
        s.close()

if __name__ == '__main__':
    conn()

