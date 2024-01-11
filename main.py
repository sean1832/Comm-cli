#!/usr/bin/env python3
import socket
import argparse
import os
import hashlib
import json

version = "0.0.4"
phrase = {
    'exit': "EXIT",
}

def handshake_send(sock, args, timeout=5):
    """
    Perform a handshake between sender and receiver.
    Returns True if the handshake is successful, False otherwise.
    """
    try:
        # Send a handshake message
        sock.sendto(b"handshake", (args.ip, args.port))
        # Wait for acknowledgment
        sock.settimeout(timeout)  # Timeout after 5 seconds
        data, _ = sock.recvfrom(1024)
        if data.decode() == "ack":
            return True
        return False
    except socket.timeout:
        print("Handshake failed: timeout")
        return False

def handshake_receive(sock):
    """
    Perform a handshake between sender and receiver.
    Returns True if the handshake is successful, False otherwise.
    """
    data, address = sock.recvfrom(1024)
    if data.decode() == "handshake":
        # Send acknowledgment
        sock.sendto(b"ack", address)
        return True
    return False

def validate_hash(path, hash):
    if get_hash(path) == hash:
        return True
    else:
        return False

def get_hash(path):
    with open(path, 'rb') as f:
        data = f.read()
        return hashlib.md5(data).hexdigest()

def send_file(args):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(f"Sending {args.file_path} to {args.ip}:{args.port}")

    print(f"Performing handshake...")
    if not handshake_send(sock, args, timeout=0.5):
        print("Ensure that the receiver is open and listening on the correct port.")
        return
    print(f"Handshake successful.")

    with open(args.file_path, 'rb') as f:
        # get file size and hash
        file_name = os.path.basename(args.file_path)
        file_size = os.path.getsize(args.file_path)
        file_hash = get_hash(args.file_path)
        metadata = {
            'name': file_name,
            'size': file_size,
            'hash': file_hash
        }
        sock.sendto(json.dumps(metadata).encode(), (args.ip, args.port))
        while True:
            data = f.read(1024)
            if not data:
                break
            sock.sendto(data, (args.ip, args.port))
            # print progress
            print(f"Progress: {f.tell()}/{file_size}", end='\r')
    print(f"\ncomplete. [{args.file_path}]")

def recieve_file(args):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', args.port))
    print(f"Listening for file on port {args.port}...")
    if not handshake_receive(sock):
        print("Handshake failed.")
        return
    # get metadata
    metadata, address = sock.recvfrom(1024)
    try:
        metadata = json.loads(metadata.decode())
    except Exception as e:
        print(f"Failed to decode metadata: {e}")
        print(f"metadata: {metadata}")
        return
    file_name = metadata['name']
    file_size = metadata['size']
    file_hash = metadata['hash']
    print(f"Receiving file from {address}...")

    with open(file_name, 'wb') as f:
        while True:
            data, address = sock.recvfrom(1024)
            if not data:
                break
            f.write(data)
            # print progress
            print(f"Progress: {f.tell()}/{file_size}", end='\r')

            # check if file is complete
            if f.tell() == file_size:
                print(f"\ncomplete. [{file_name}]")
                break
    print(f"Validating file...")
    try:
        if validate_hash(file_name, file_hash):
            print(f"File validated.")
        else:
            print(f"File validation failed! Expected {file_hash} but got {get_hash(file_name)}.")
    except Exception as e:
        print(f"File validation failed! {e}")

def recieve_files(args):
        while True:
            recieve_file(args)

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
        if message == phrase['exit']:
            break

def sender(args):
    if args.file_path:
        send_file(args)
    else:
        send_messages(args)

def receiver(args):
    if args.file_path:
        recieve_files(args) if args.recursive else recieve_file(args)
    else:
        receive_messages(args)


def main():
    parser = argparse.ArgumentParser(description=f"UDP Chat Application v{version}")
    parser.add_argument('-v', '--version', action='store_true', help='Get current version')
    parser.add_argument('--get-ip', action='store_true', help='Get local IP address')
    subparsers = parser.add_subparsers(dest='command')

    # Sub-parser for receive
    receive_parser = subparsers.add_parser('get')
    receive_parser.add_argument('-p', '--port', type=int, help='Port number')
    receive_parser.add_argument('-a', '--annomyous', action='store_true', help='Annomyous mode (no IP address)')
    receive_parser.add_argument('-f', '--file-path', type=str, help='File directory to save to, use "." to save to current directory.')
    receive_parser.add_argument('-r', '--recursive', action='store_true', help='Recursive mode (keep listening)')
    receive_parser.set_defaults(func=receiver)

    # Sub-parser for send
    send_parser = subparsers.add_parser('post')
    send_parser.add_argument('-i', '--ip', type=str, required=True, help='Target IP address')
    send_parser.add_argument('-p', '--port', type=int, help='Port number')
    send_parser.add_argument('-f', '--file-path', type=str, help='File path to send')
    send_parser.set_defaults(func=sender)

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