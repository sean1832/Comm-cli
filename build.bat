@echo off
if not exist dist (
  mkdir dist
)
copy main.py dist\udp-chat.py
echo Build completed at dist\udp-chat.py.