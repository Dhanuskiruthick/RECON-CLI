import socket
import threading

open_ports = []


def scan_port(target, port):

    try:
        sock = socket.socket()
        sock.settimeout(0.5)

        result = sock.connect_ex((target, port))

        if result == 0:
            open_ports.append(port)

        sock.close()

    except:
        pass


def scan_ports(target, start_port, end_port):

    threads = []

    for port in range(start_port, end_port + 1):

        thread = threading.Thread(
            target=scan_port,
            args=(target, port)
        )

        threads.append(thread)

        thread.start()

    for thread in threads:
        thread.join()

    return open_ports