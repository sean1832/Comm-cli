import socket
import json
import os
import time

from nx import utilities as utils

def send_file_udp(ip, port, file_path, chunk, verbose=False):
    chunk = chunk * 1024 # convert to bytes
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    if verbose: print("UDP Socket created.")
    if verbose: print(f"Sending {file_path} to {ip}:{port}")

    if verbose: print(f"Performing handshake...")
    if not utils.handshake_send(sock, ip, port, timeout=0.5):
        print("Ensure that the receiver is open and listening on the correct port.")
        return
    if verbose: print(f"Handshake successful.")

    # send metadata
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    file_hash = utils.get_hash(file_path)
    metadata = {
        'name': file_name,
        'size': file_size,
        'hash': file_hash
    }
    msg = "Sending metadata..."
    if verbose: print(f"Sending metadata...", end='\r')
    sock.sendto(json.dumps(metadata).encode(), (ip, port))
    if verbose: print("Metadata sent.".ljust(len(msg)))

    # send file
    if verbose: print("Sending file...")
    start_time = time.time()
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(chunk)
            if not data:
                break
            sock.sendto(data, (ip, port))
            # print progress
            utils.print_progress(f.tell(), file_size, verbose, unit='auto')
    end_time = time.time()
    print(f"\ncomplete in {round(end_time - start_time, 2)} seconds. [{file_path}]") 

def recieve_file_udp(port, save_dir, chunk, verbose=False):
    chunk = chunk * 1024 # convert to bytes
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    if verbose: print("UDP Socket created.")
    sock.bind(('0.0.0.0', port))
    print(f"Listening for file on port {port}...")

    if verbose: print('Performing handshake...')
    if not utils.handshake_receive(sock):
        print("Handshake failed.")
        return
    if verbose: print("Handshake successful.")

    # get metadata
    msg = "Waiting for metadata..."
    if verbose: print(msg, end='\r')
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
    if verbose: print("Metadata received.".ljust(len(msg)))

    file_path = os.path.join(save_dir, file_name)
    # create directory if it doesn't exist
    os.makedirs(save_dir, exist_ok=True)

    start_time = time.time()
    try:
        with open(file_path, 'wb') as f:
            if verbose: print(f"Receiving file from {address}...")
            while True:
                data, address = sock.recvfrom(chunk)
                if not data:
                    break
                f.write(data)

                # print progress
                utils.print_progress(f.tell(), file_size, verbose, unit='auto')

                # set timeout to 3 seconds
                sock.settimeout(3)
                # check if file is complete
                if f.tell() == file_size:
                    break
        end_time = time.time()
        print(f"\ncomplete in {round(end_time - start_time, 2)} seconds. [{file_path}]") 
    except socket.timeout:
        print(f"File transfer timed out.")
        return
    except socket.error as e:
        print(f"File transfer failed: {e}")
        return
    finally:
        sock.close()
        if verbose: print("UDP Socket closed.")
    
    msg = 'Validating file...'
    print(f"Validating file...", end='\r')
    try:
        if utils.validate_hash(file_path, file_hash):
            print(f"File validated.".ljust(len(msg)))
        else:
            print(f"File validation failed! Expected {file_hash} but got {utils.get_hash(file_path)}.")
    except Exception as e:
        print(f"File validation failed! {e}")

def recieve_files_udp(port, save_dir, chunk, verbose=False):
    try:
        while True:
            recieve_file_udp(port, save_dir, chunk, verbose=verbose)
    except KeyboardInterrupt:
        print("Manual Exit.")
        return