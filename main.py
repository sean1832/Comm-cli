#!/usr/bin/env python3
import socket
import argparse
import threading

version = "0.0.2"

def init_handshake(sock, target_address):
    if target_address:
        sock.sendto("READY".encode(), target_address)
    print("Waiting for server to be ready...")
    while True:
        try:
            message, address = sock.recvfrom(1024)
            if message.decode() == "READY":
                print("Handshake completed. Ready for communication.")
                break
        except OSError as e:
            print(f"Error receiving message: {e}")
            break

def receive_messages(sock):
    while True:
        message, address = sock.recvfrom(1024)
        print(f"Message from {address}: {message.decode()}")

def send_messages(sock, target_address):
    while True:
        message = input("Enter message to send: ")
        sock.sendto(message.encode(), target_address)

def run_application(mode, address, port, verbose):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', port) if mode == 'server' else ('0.0.0.0', 0))

    target_address = (address, port) if mode == 'client' else None
    init_handshake(sock, target_address)

    threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()
    send_messages(sock, target_address)

def get_local_ip():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(('10.255.255.255', 1))
        IP = sock.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        sock.close()
    return IP

def main():
    parser = argparse.ArgumentParser(description="UDP Chat Application")
    parser.add_argument('--get-ip', action='store_true', help='Get local IP address')
    parser.add_argument('-v', '--version', action='store_true', help='Get current version')
    parser.add_argument('-i', '--ip', type=str, default='', help='IP address of the other party (empty for server mode)')
    parser.add_argument('-p', '--port', type=int, default=12345, help='Port number')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose mode')

    args = parser.parse_args()

    if args.version:
        print(f"{version}")
    elif args.get_ip:
        print(f"Local IP Address: {get_local_ip()}")
    else:
        mode = 'client' if args.ip else 'server'
        run_application(mode, args.ip, args.port, args.verbose)

if __name__ == "__main__":
    main()
