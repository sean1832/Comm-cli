## About
This is a simple program that allows two computer under the same network to communicate with each other in terminal using udp protocol. It is useful for copy and paste text between two computer.

## How to use
1. Download the [latest release]()
2. Get the ip address computer A
```shell
./udp-chat --get-ip
```
3. Run the program on the computer A
```shell
./udp-chat client --port 50000
```
4. Run the program on the computer B
```shell
./udp-chat server --port 50000 --ip <ip address of computer A>
```

## For developer
### How to build
##### **UNIX**
2. Elevate privileges `chmod +x build.sh`
3. Run `./build.sh`

##### **Windows**
2. Run `build.bat`