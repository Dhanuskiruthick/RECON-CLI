import socket

target = input("Enter target: ")

common_ports = {
    21: "FTP",
    22: "SSH",
    80: "HTTP",
    443: "HTTPS",
    3306: "MySQL"
}

print(f"\nScanning {target}...\n")

for port, service in common_ports.items():

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)

    result = sock.connect_ex((target, port))

    if result == 0:
        print(f"[OPEN] {port} → {service}")

    sock.close()
