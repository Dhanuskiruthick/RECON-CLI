import socket

target = input("Enter target: ")
port = int(input("Enter port: "))

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.settimeout(3)

try:
    sock.connect((target, port))

    banner = sock.recv(1024)

    print("\n[BANNER RECEIVED]")
    print(banner.decode(errors="ignore"))

except:
    print("\n[ERROR] Could not connect to target")

sock.close()    