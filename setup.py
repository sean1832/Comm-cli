from setuptools import setup

setup(
    name='nx',
    version='0.0.8',
    author='Zeke Zhang',
    description='Simple local network data transfer CLI. Supports file transfer (udp and tcp) and text transfer.',
    scripts=['main.py', 'progress_bar.py', 'utilities.py'],
    entry_points={
        'console_scripts': [
            'nx = main:main',
        ],
    },
)