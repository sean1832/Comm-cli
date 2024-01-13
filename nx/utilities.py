import hashlib
import json
import socket
import os

import nx.progress_bar as pb

def read_manifest():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    manifest_path = os.path.join(dir_path, 'manifest.json')
    with open(manifest_path, 'r') as f:
        return json.load(f)

def handshake_send(sock, ip, port, timeout=5):
    """
    Perform a handshake between sender and receiver.
    Returns True if the handshake is successful, False otherwise.
    """
    try:
        # Send a handshake message
        sock.sendto(b"handshake", (ip, port))
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
    try:
        data, address = sock.recvfrom(1024)
        if data.decode() == "handshake":
            sock.sendto(b"ack", address)
            return True
        return False
    except socket.error as e:
        print(f"Handshake failed: {e}")
        return False

def validate_hash(path, hash_value):
    return get_hash(path) == hash_value

def get_hash(path):
    with open(path, 'rb') as f:
        data = f.read()
        return hashlib.md5(data).hexdigest()

def print_progress(iteration, total, verbose, unit='kb'):
        sent_data = convert_byte(iteration, unit)
        total_data = convert_byte(total, unit)
        description = f"({total_data} kb)"
        if verbose: description = f"({sent_data}/{total_data} {unit})"
        pb.progress_bar(iteration, total, description=description)



def convert_byte(byte, unit, percision: int=2):
    '''
    Convert byte to KB, MB, GB
    '''
    unit = unit.upper()

    if unit == 'KB':
        return round(byte / 1024, percision)
    elif unit == 'MB':
        return round(byte / (1024 * 1024), percision)
    elif unit == 'GB':
        return round(byte / (1024 * 1024 * 1024), percision)
    else:
        raise ValueError(f'Invalid unit {unit}')