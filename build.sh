if [ ! -d "dist" ]; then
  mkdir dist
fi
cp main.py dist/udp-chat
chmod +x dist/udp-chat
echo "Build completed at dist/udp-chat."