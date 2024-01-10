# UDP Chat

## Overview
UDP Chat is a lightweight, terminal-based chat application enabling text communication over a local network. It uses the UDP protocol for message transmission. This tool is effective for transferring text data quickly between two computers in the same network environment.

## Getting Started

### Prerequisites
- Python 3.x installed on your system
- Network connectivity between the two computers

### Installation
1. Clone the repository.
```bash
git clone https://github.com/sean1832/udp-chat.git
```
2. Navigate to the source directory.
3. Run the installation script (`install.sh` on UNIX, `install.bat` on Windows).
> Note: On UNIX systems, you need to ensure that the script has executable permissions. You can do this by running `chmod +x install.sh` from the terminal.

### Usage
Run the program from the terminal or command prompt.

#### Receiving Messages
1. On the receiver's computer, execute:
   ```
   udp-chat get --port PORT_NUMBER
   ```
   Replace `PORT_NUMBER` with the desired port number.

#### Sending Messages
1. On the sender's computer, execute:
   ```
   udp-chat post --ip RECEIVER_IP --port PORT_NUMBER
   ```
   Replace `RECEIVER_IP` with the receiver's IP address and `PORT_NUMBER` with the port number used by the receiver.

### Options
- `-i`, `--version` : Displays the current version of the application.
- `--get-ip` : Retrieves the local IP address of your computer.
- `-a`, `--annomyous` : For receivers, hides the sender's IP address from the message display.

## Contributing
Contributions are welcome. Please follow the standard fork and pull request workflow.

## License
This project is licensed under [Apache License 2.0](LICENSE). See the LICENSE file for details.
