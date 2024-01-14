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

def print_progress(iteration, total, verbose, unit='auto'):
        sent_data = convert_byte(iteration, unit)
        total_data = convert_byte(total, unit)
        description = f"({total_data[0]} {total_data[1]})"
        if verbose: description = f"({sent_data}/{total_data} {total_data[1]})"
        pb.progress_bar(iteration, total, description=description)



def convert_byte(byte, unit, percision: int=2):
    '''
    Convert byte to KB, MB, GB
    '''
    unit = unit.lower()

    kb = byte / 1024
    mb = kb / 1024
    gb = mb / 1024

    if unit == 'kb':
        return round(kb, percision), 'kb'
    elif unit == 'mb':
        return round(mb, percision), 'mb'
    elif unit == 'gb':
        return round(gb, percision), 'gb'
    elif unit == 'auto':
        if gb > 1:
            return round(gb, percision), 'gb'
        elif mb > 1:
            return round(mb, percision), 'mb'
        elif kb > 1:
            return round(kb, percision), 'kb'
        else:
            return round(byte, percision), 'b'
    else:
        raise ValueError(f'Invalid unit {unit}')