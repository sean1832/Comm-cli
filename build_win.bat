@echo off

pyinstaller gui_win.spec

echo "Post build: Copying files to dist folder"
python scripts/post_build.py