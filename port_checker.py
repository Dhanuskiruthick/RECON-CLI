import socket

target = input("Enter target IP/domain: ")
port = int(input("Enter port: "))

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.settimeout(3)

result = sock.connect_ex((target, port))

if result == 0:
    print(f"\n[OPEN] Port {port} is open on {target}")
else:
    print(f"\n[CLOSED] Port {port} is closed on {target}")

sock.close()