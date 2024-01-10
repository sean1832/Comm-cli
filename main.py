#!/usr/bin/env python3
import socket
import argparse

version = "0.0.3"
phrase = {
    'exit': "EXIT",
}

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def receive_messages(args):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', args.port))
    print(f"Listening for messages on port {args.port}...")

    while True:
        message, address = sock.recvfrom(1024)
        if message.decode() == phrase['exit']:
            break
        print(f"Message from {address}: {message.decode()}")

def send_messages(args):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(f"Sending messages to {args.ip}:{args.port}")

    while True:
        message = input("Enter message to ssend: ")
        sock.sendto(message.encode(), (args.ip, args.port))
        if message == phrase['exit']:
            break

def main():
    parser = argparse.ArgumentParser(description=f"UDP Chat Application v{version}")
    parser.add_argument('-v', '--version', action='store_true', help='Get current version')
    parser.add_argument('--get-ip', action='store_true', help='Get local IP address')
    subparsers = parser.add_subparsers(dest='command')

    # Sub-parser for receive
    receive_parser = subparsers.add_parser('get')
    receive_parser.add_argument('-p', '--port', type=int, help='Port number')
    receive_parser.set_defaults(func=receive_messages)

    # Sub-parser for send
    send_parser = subparsers.add_parser('post')
    send_parser.add_argument('-i', '--ip', type=str, required=True, help='Target IP address')
    send_parser.add_argument('-p', '--port', type=int, help='Port number')
    send_parser.set_defaults(func=send_messages)

    args = parser.parse_args()

    if args.version:
        print(f"{version}")
    elif args.get_ip:
        print(f"{get_local_ip()}")
    elif hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()