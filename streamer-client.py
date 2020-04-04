import socket

addr = ("127.0.0.1",9999)
def conn():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.sendto("streamer".encode("utf-8"), addr)
        data, _ = s.recvfrom(1024)
        print(data.decode("utf-8"))
        while True:
            output = input()
            s.sendto(("streamer:"+output).encode("utf-8"),addr)
            print("send>>> ", output)
    except Exception as e:
        print(e)
    finally:
        s.close()

if __name__ == '__main__':
    conn()

