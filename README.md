# Network Data Exchanger (nx-cli)

## 1. Overview 📋
Network Data Exchanger (nx-cli) is a versatile command-line tool 🛠️ for sending and receiving messages and binary files over a network. It supports both UDP and TCP protocols and is primarily designed for use on local networks. This tool functions similarly to macOS's Airdrop, providing an efficient method for data transfer between computers on the same network.

## 2. Features 🌟
- **Plaintext Message Transfer:** Easily send plaintext contents from one computer to another within the same network.

- **File Sharing:** Quickly transfer files between computers without the need for USB drives or third-party websites like emails or messaging apps.

- **UDP and TCP Protocol Support:** Flexibility to choose between UDP for faster transfers or TCP for more reliable transmission. *(TCP is the default protocol)*

- **Local IP Retrieval:** Conveniently find out your computer's local IP address without needing to run `ipconfig` or `ifconfig`.

- **Cross-Platform Compatibility:** Functions on any system with Python 3.x, enhancing versatility.


## 3. Getting Started 🚀

### Prerequisites 📝
- Python 3.x installed on your system.
- Network connectivity between the computers involved.

### Installation 🔧
1. Clone the repository:
   ```bash
   git clone https://github.com/sean1832/nx-cli.git
   ```
2. Navigate to the source directory.
3. Install the package:
   ```bash
   pip install .
   ```

## 4. Usage 📖
Run nx-cli from the terminal or command prompt using various commands to send or receive data.

#### Get Local IP 🌐
Retrieve your computer's local IP address:
   ```bash
   nx ip
   ```
> 📝 **Note:** Each computer's IP is unique. To send data, you need the IP of the receiving computer. Ensure both computers are on the same network.

#### Sending Files 📤

To send a file:
   ```bash
   nx post file RECEIVER_IP PORT_NUMBER FILE_PATH [--udp]
   ```
Replace `RECEIVER_IP`, `PORT_NUMBER`, and `FILE_PATH` with the appropriate values.
- Use `--udp` for UDP transmission.
> it is recommended to use TCP for file transfers to ensure reliability. UDP is faster but may result in data loss.

#### Receiving Files 📥
To receive a file:
   ```bash
   nx get file PORT_NUMBER SAVE_DIRECTORY [--udp] [--recursive]
   ```
Replace `PORT_NUMBER` and `SAVE_DIRECTORY` with the desired port and directory path. 
> `.` can be used to save the file in the current directory.
- Use `--udp` for UDP transmission. *(If sender uses `udp`, the receiver must also use `udp` to receive data.)*
- Use `-r` or `--recursive` for continuous reception.

#### Sending Messages 💬
To send a message:
   ```bash
   nx post msg --ip RECEIVER_IP --port PORT_NUMBER
   ```
Replace `RECEIVER_IP` and `PORT_NUMBER` with the receiver's IP address and port number.

#### Receiving Messages 📨
To receive a message:
   ```bash
   nx get msg PORT_NUMBER [-a]
   ```
Replace `PORT_NUMBER` with the desired port number.
- Use `-a` for anonymous mode, hiding the sender's IP.

### Options ⚙️
- `-v`, `--version`: Displays the current version of the application.

## 5. Contributing 🤝
Contributions are welcome! Please follow the standard fork-and-pull-request workflow.

## 6. License 📄
This project is licensed under the [Apache License 2.0](LICENSE). See the LICENSE file for more details.