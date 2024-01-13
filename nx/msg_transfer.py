import socket

EXIT = "EXIT"

def receive_messages(args):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', args.port))
    print(f"Listening for messages on port {args.port}...")

    while True:
        message, address = sock.recvfrom(1024)
        if message.decode() == EXIT:
            break
        if args.annomyous:
            print(f"{message.decode()}")
        else:
            print(f"Message from {address}: {message.decode()}")

def send_messages(args):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(f"Sending messages to {args.ip}:{args.port}")

    while True:
        message = input("send: ")
        sock.sendto(message.encode(), (args.ip, args.port))
        if message == EXIT:
            break