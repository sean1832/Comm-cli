import socket
from nx.udp_transfer import send_file_udp, recieve_file_udp, recieve_files_udp
from nx.tcp_transfer import send_file_tcp, recieve_file_tcp, recieve_files_tcp
from nx.msg_transfer import send_messages, receive_messages



def get_local_ip(*args, **kwargs):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    print(f"{IP}")

def send_file(args):
    ip = args.ip
    port = args.port
    file_path = args.file_path
    verbose = args.verbose
    chunk = args.chunk
    if args.udp: 
        send_file_udp(ip, port, file_path, chunk, verbose=verbose)
    else:
        send_file_tcp(ip, port, file_path, chunk, verbose=verbose)
    

def recieve_file(args):
    port = args.port
    file_dir = args.file_dir
    chunk = args.chunk
    if args.verbose:
        verbose = True
    else:
        verbose = False
    if args.udp:
        if args.recursive:
            recieve_files_udp(port, file_dir, chunk, verbose=verbose)
        else:
            recieve_file_udp(port, file_dir, chunk, verbose=verbose)
    else:
        if args.recursive:
            recieve_files_tcp(port, file_dir, chunk,  verbose=verbose)
        else:
            recieve_file_tcp(port, file_dir, chunk, verbose=verbose)