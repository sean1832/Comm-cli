@echo off
if not exist dist (
    mkdir dist
)
copy main.py dist\udp-chat.py
echo @python "%~dp0dist\udp-chat.py" %*>dist\udp-chat.bat
echo Build completed at dist\udp-chat.bat.