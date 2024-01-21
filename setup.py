import json

from setuptools import find_packages, setup

manifest = json.load(open("nx/manifest.json", "r"))

setup(
    name=manifest["name"],
    version=manifest["version"],
    author=manifest["author"],
    description=manifest["description"],
    url=manifest["url"],
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "": [
            "manifest.json",
            "assets/toggle_on.png",
            "assets/toggle_off.png",
            "assets/icon.png",
            "assets/icon.ico",
        ]
    },
    install_requires=[
        "PySide6",
    ],
    entry_points={
        "console_scripts": [
            "nx = nx.cli.cli_main:main",
            "nx-gui = nx.gui.gui_main:main",
        ],
    },
)
