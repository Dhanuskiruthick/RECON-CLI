import socket


def get_http_headers(target):

    try:

        sock = socket.socket()

        sock.settimeout(3)

        sock.connect((target, 80))

        request = (
            "GET / HTTP/1.1\r\n"
            f"Host: {target}\r\n"
            "Connection: close\r\n\r\n"
        )

        sock.send(request.encode())

        response = sock.recv(4096).decode(errors="ignore")

        sock.close()

        return response

    except:

        return None