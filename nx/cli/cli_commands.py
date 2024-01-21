import nx.core.utilities as utils
from nx.core.msg_transfer import receive_messages, send_messages  # noqa: F401
from nx.core.tcp_transfer import receive_file_tcp, send_file_tcp


def get_local_ip(*args, **kwargs):
    ip = utils.get_local_ip()
    print(f"{ip}")


def send_file(args):
    ip = args.ip
    port = args.port
    file_path = args.file_path
    verbose = args.verbose
    chunk = args.chunk
    zip_mode = args.zip
    for progress in send_file_tcp(
        ip, port, file_path, chunk, zip_mode, verbose=verbose
    ):
        utils.print_progress(
            progress["current"],
            progress["total"],
            title="Sending",
            verbose=verbose,
            unit="auto",
        )


def recieve_file(args):
    port = args.port
    file_dir = args.file_dir
    chunk = args.chunk
    if args.verbose:
        verbose = True
    else:
        verbose = False
    for progress in receive_file_tcp(port, file_dir, chunk, verbose=verbose):
        utils.print_progress(
            progress["current"],
            progress["total"],
            title="Receiving",
            verbose=verbose,
            unit="auto",
        )
