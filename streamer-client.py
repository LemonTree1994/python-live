import socket

addr = ('127.0.0.1', 9999)
def conn():
    s = socket.socket()
    try:
        #establish connection
        s.connect(addr)
        data = s.recv(1024)
        print(data.decode("utf-8"))
        s.send("streamer".encode("utf-8"))
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

