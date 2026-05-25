import socket

def resolve_target(target):

    try:
        ip = socket.gethostbyname(target)
        return ip

    except:
        return None