import socket

target = input("Enter target : ")

ports = [21, 22, 80, 443, 3306]

print(f"\n==== Scanning {target} ====\n")

for port in ports:

    try:

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.settimeout(1)

        result = sock.connect_ex((target, port))

        if result == 0:
            print(f"[OPEN] Port {port} is open on {target}")

        else:
            print(f"[CLOSED] Port {port} is closed on {target}")

        sock.close()

    except Exception as e:

        print(f"[ERROR] Port {port} -> {e}")