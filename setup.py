from setuptools import setup

setup(
    name='nx',
    version='0.0.5',
    author='Zeke Zhang',
    description='Simple local network data transfer CLI. Supports file transfer (udp and tcp) and text transfer.',
    scripts=['main.py'],
    entry_points={
        'console_scripts': [
            'nx = main:main',
        ],
    },
)