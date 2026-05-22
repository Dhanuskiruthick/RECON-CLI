import socket  # python networking module

domain = input("Enter domain : ")
 
ip = socket.gethostbyname(domain)

print(f"\nIP address of {domain} is {ip}")