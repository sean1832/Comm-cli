#!/bin/bash
pyinstaller gui_mac.spec

echo "Post build: Copying files to dist folder"
python3 scripts/post_build.py