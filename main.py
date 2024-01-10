#!/usr/bin/env python3
import socket
import argparse
import threading

version = "0.0.1"

def receive_messages(sock):
    while True:
        message, address = sock.recvfrom(1024)
        print(f"Message from {address}: {message.decode()}")

def send_messages(sock, target_address):
    while True:
        message = input("Enter message to send: ")
        sock.sendto(message.encode(), target_address)

def run_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('0.0.0.0', port))
    print(f"UDP Server listening on port {port}")

    threading.Thread(target=receive_messages, args=(server_socket,), daemon=True).start()
    send_messages(server_socket, ('<CLIENT_IP_ADDRESS>', port))

def run_client(server_ip, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()
    send_messages(client_socket, (server_ip, port))

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

def main():
    parser = argparse.ArgumentParser(description="UDP Chat Application")
    parser.add_argument('--get-ip', action='store_true', help='Get local IP address')
    parser.add_argument('-v', '--version', action='store_true', help='Get current version')
    subparsers = parser.add_subparsers(dest='mode')

    # Server parser
    server_parser = subparsers.add_parser('server')
    server_parser.add_argument('-p', '--port', type=int, default=12345, help='Port number')

    # Client parser
    client_parser = subparsers.add_parser('client')
    client_parser.add_argument('-i', '--ip', type=str, required=True, help='Server IP address')
    client_parser.add_argument('-p', '--port', type=int, default=12345, help='Port number')

    args = parser.parse_args()

    if args.version:
        print(f"{version}")
    elif args.get_ip:
            print(f"Local IP Address: {get_local_ip()}")
    elif args.mode == 'server':
        run_server(args.port)
    elif args.mode == 'client':
        run_client(args.ip, args.port)
    elif args.mode is None:
        print("No mode specified. Use --help for more information.")
    else:
        print(f"Unknown mode: {args.mode}")

if __name__ == "__main__":
    main()