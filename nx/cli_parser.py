import argparse

from nx.cli_commands import get_local_ip, send_messages, receive_messages, send_file, recieve_file
from nx.utilities import read_manifest

def build_parser():
    parser = argparse.ArgumentParser(description=f"Network Data Exchanger (nx-cli) v{read_manifest()['version']}")
    parser.add_argument('-v', '--version', action='store_true', help='Print version')
    subparsers = parser.add_subparsers(dest='command')

    # Get local IP command parser
    get_ip_parser = subparsers.add_parser('ip', help='Get local IP address')
    get_ip_parser.set_defaults(func=get_local_ip)

    # Post command parser
    post_parser = subparsers.add_parser('post', help='Send data')
    post_subparsers = post_parser.add_subparsers(dest='type')

    # Post message
    post_msg_parser = post_subparsers.add_parser('msg', help='Send plaintext messages')
    post_msg_parser.add_argument('ip', type=str, help='Target IP address')
    post_msg_parser.add_argument('port', type=int, help='Port number')
    post_msg_parser.set_defaults(func=send_messages)

    # Post file
    post_file_parser = post_subparsers.add_parser('file', help='Send files as binary')
    post_file_parser.add_argument('ip', type=str, help='Target IP address')
    post_file_parser.add_argument('port', type=int, help='Port number')
    post_file_parser.add_argument('file_path', type=str, help='File path to send')
    post_file_parser.add_argument('--udp', action='store_true', help='Use UDP instead of TCP. Faster but less reliable.')
    post_file_parser.add_argument('-c', '--chunk', type=int, help='Chunk size in kb for file transfer. Default 4. Recommended between 4 to 64 kb.', default=4)
    post_file_parser.add_argument('-z', '--zip', action='store_true', help='Zip before sending. Only works for directories.')
    post_file_parser.add_argument('--verbose', action='store_true', help='Print verbose output')
    post_file_parser.set_defaults(func=send_file)

    # Get command parser
    get_parser = subparsers.add_parser('get', help='Receive data')
    get_subparsers = get_parser.add_subparsers(dest='type')

    # Get message
    get_msg_parser = get_subparsers.add_parser('msg', help='Receive plaintext messages')
    get_msg_parser.add_argument('port', type=int, help='Port number')
    get_msg_parser.add_argument('-a', '--annomyous', action='store_true', help='Receive messages annomyously')
    get_msg_parser.set_defaults(func=receive_messages)

    # Get file
    get_file_parser = get_subparsers.add_parser('file', help='Receive files as binary')
    get_file_parser.add_argument('port', type=int, help='Port number')
    get_file_parser.add_argument('file_dir', type=str, help='File directory to save to')
    get_file_parser.add_argument('-r', '--recursive', action='store_true', help='Receive files recursively')
    get_file_parser.add_argument('--udp', action='store_true', help='Use UDP instead of TCP. Faster but less reliable.')
    get_file_parser.add_argument('-c', '--chunk', type=int, help='Chunk size in kb for file transfer. Default 4. Recommended between 4 to 64.', default=4)
    get_file_parser.add_argument('--verbose', action='store_true', help='Print verbose output')
    get_file_parser.set_defaults(func=recieve_file)

    return parser