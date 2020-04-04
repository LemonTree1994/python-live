import socket
import threading
import time

addr = ("127.0.0.1",8888)
def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:

        streamername = input("enter the streamer name to watch the live:")
        s.sendto(f"sub:{streamername}".encode("utf-8"), addr)
        data, _ = s.recvfrom(1024)
        data = data.decode("utf-8")
        print(data)
        if data == "error":
            return
        #receive  message
        while True:
            data, _ = s.recvfrom(1024)
            print("recv>>> ", data.decode("utf-8"))
    except Exception as e:
        print(e)
    finally:
        s.close()

if __name__ == '__main__':
    main()
