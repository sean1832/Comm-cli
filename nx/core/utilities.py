import hashlib
import json
import os
import socket
import zipfile

from . import progress_bar as pb


def read_manifest():
    dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    manifest_path = os.path.join(dir_path, "manifest.json")
    with open(manifest_path, "r") as f:
        return json.load(f)


def read_json(path):
    with open(path, "r") as f:
        return json.load(f)


def write_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


def get_project_root():
    return os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def get_appdata_path():
    if os.name == "nt":  # Windows
        return str(os.getenv("APPDATA"))
    elif os.name == "posix":  # Linux or Mac
        return str(os.path.expanduser("~"))
    else:  # Unsupported OS
        raise OSError(f"Unsupported OS: {os.name}")


def get_appdata_root():
    return os.path.join(get_appdata_path(), "nx")


def read_local_entries(data_source) -> list[str]:
    root = get_appdata_root()
    data_file = os.path.join(root, data_source)
    # create directory if it doesn't exist
    os.makedirs(os.path.dirname(data_file), exist_ok=True)

    # if data file doesn't exist, write empty list
    if (
        not os.path.exists(data_file)
        or read_json(data_file) is None
        or len(read_json(data_file)) == 0
    ):
        write_json(data_file, [""])

    return read_json(data_file)


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(("10.255.255.255", 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


def zip_dir(dir_path, zip_path, chunk_size=1024 * 1024 * 20):
    total_size = sum(
        [
            os.path.getsize(os.path.join(root, file))
            for root, _, files in os.walk(dir_path)
            for file in files
        ]
    )
    processed_size = 0

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, os.path.join(dir_path, ".."))

                # Create a ZipInfo object for the file
                zip_info = zipfile.ZipInfo(rel_path)
                zip_info.compress_type = zipfile.ZIP_DEFLATED
                zip_info.file_size = os.path.getsize(file_path)

                # Open the file and read in chunks
                with open(file_path, "rb") as source, zipf.open(
                    zip_info, "w"
                ) as target:
                    while True:
                        data = source.read(chunk_size)
                        if not data:
                            break
                        target.write(data)

                        processed_size += len(data)
                        print_progress(
                            processed_size,
                            total_size,
                            title="Zipping",
                            verbose=True,
                            unit="auto",
                        )
    return zip_path


def unzip_dir(zip_path, dir_path):
    with zipfile.ZipFile(zip_path, "r") as zipf:
        zipf.extractall(dir_path)


def handshake_send(sock, ip, port, timeout: float | int = 5):
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
    with open(path, "rb") as f:
        data = f.read()
        return hashlib.md5(data).hexdigest()


def print_progress(iteration, total, title="progress", verbose=False, unit="auto"):
    sent_data = convert_byte(iteration, unit)
    total_data = convert_byte(total, unit)
    description = f"({total_data[0]} {total_data[1]})"
    if verbose:
        description = f"({sent_data[0]} {sent_data[1]}/{total_data[0]} {total_data[1]})"
    pb.progress_bar(iteration, total, title=title, description=description)


def convert_byte(byte, unit, percision: int = 2):
    """
    Convert byte to KB, MB, GB
    """
    unit = unit.lower()

    kb = byte / 1024
    mb = kb / 1024
    gb = mb / 1024

    if unit == "kb":
        return round(kb, percision), "kb"
    elif unit == "mb":
        return round(mb, percision), "mb"
    elif unit == "gb":
        return round(gb, percision), "gb"
    elif unit == "auto":
        if gb > 1:
            return round(gb, percision), "gb"
        elif mb > 1:
            return round(mb, percision), "mb"
        elif kb > 1:
            return round(kb, percision), "kb"
        else:
            return round(byte, percision), "b"
    else:
        raise ValueError(f"Invalid unit {unit}")
