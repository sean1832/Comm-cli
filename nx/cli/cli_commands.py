import socket

from nx.core.msg_transfer import receive_messages, send_messages  # noqa: F401
from nx.core.tcp_transfer import recieve_file_tcp, send_file_tcp


def get_local_ip(*args, **kwargs):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(("10.255.255.255", 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = "127.0.0.1"
    finally:
        s.close()
    print(f"{IP}")


def send_file(args):
    ip = args.ip
    port = args.port
    file_path = args.file_path
    verbose = args.verbose
    chunk = args.chunk
    zip_mode = args.zip
    send_file_tcp(ip, port, file_path, chunk, zip_mode, verbose=verbose)


def recieve_file(args):
    port = args.port
    file_dir = args.file_dir
    chunk = args.chunk
    if args.verbose:
        verbose = True
    else:
        verbose = False
    recieve_file_tcp(port, file_dir, chunk, verbose=verbose)
