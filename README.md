# NetXchanger (nx)
<img src="nx/assets/icon.png" width="160">

## 1. Overview 📋
NetXchanger is a versatile tool 🛠️ for sending and receiving binary files over a network. This tool functions similarly to macOS's Airdrop, but does not limit to macOS devices. NetXchanger is a CLI tool, but also has a GUI version for Windows and macOS.

## 2. Features 🌟
- **Plaintext Message Transfer:** Easily send plaintext contents from one computer to another within the same network. (Only available in CLI version)

- **File Sharing:** Quickly transfer files between computers without the need for USB drives or third-party websites like emails or messaging apps.

- **Local IP Retrieval:** Conveniently find out your computer's local IP address without needing to run `ipconfig` or `ifconfig`.

- **Cross-Platform Compatibility:** Functions on any system with Python 3.x, enhancing versatility. (GUI version only works on Windows and macOS)


## 3. Getting Started 🚀

### Prerequisites 📝
- Python 3.x installed on your system.
- Network connectivity between the computers involved.

### GUI Installation 🔧
1. Download the latest release from the [releases page](https://github.com/sean1832/nx-cli/releases/latest) depending on your operating system.
2. Extract the contents of the zip file and run the executable.

### CLI Installation 🔧
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
Run `nx` from the terminal or command prompt using various commands to send or receive data.

### GUI
To run the GUI version of the application, run `nx-gui` from the terminal or command prompt.
```bash
nx-gui
```

#### Get Local IP 🌐
Retrieve your computer's local IP address:
   ```bash
   nx ip
   ```
> 📝 **Note:** Each computer's IP is unique. To send data, you need the IP of the receiving computer. Ensure both computers are on the same network.

#### Sending Files 📤

To send a file:
   ```bash
   nx post file RECEIVER_IP PORT_NUMBER FILE_PATH
   ```
Replace `RECEIVER_IP`, `PORT_NUMBER`, and `FILE_PATH` with the appropriate values.

#### Receiving Files 📥
To receive a file:
   ```bash
   nx get file PORT_NUMBER SAVE_DIRECTORY
   ```
Replace `PORT_NUMBER` and `SAVE_DIRECTORY` with the desired port and directory path. 
> `.` can be used to save the file in the current directory.

#### Sending Directories 📂
To send a directory:
   ```bash
   nx post file RECEIVER_IP PORT_NUMBER DIR_PATH -z
   ```
- Use `-z` to zip the directory before sending.

#### Sending Messages 💬
To send a message:
   ```bash
   nx post msg --ip RECEIVER_IP --port PORT_NUMBER
   ```

#### Receiving Messages 📨
To receive a message:
   ```bash
   nx get msg PORT_NUMBER [-a]
   ```
- Use `-a` for anonymous mode, hiding the sender's IP.

### Options ⚙️
- `-v`, `--version`: Displays the current version of the application.

## 5. Contributing 🤝
Contributions are welcome! Please follow the standard fork-and-pull-request workflow.

## 6. License 📄
This project is licensed under the [Apache License 2.0](LICENSE). See the LICENSE file for more details.