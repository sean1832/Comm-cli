from importlib.metadata import entry_points
from setuptools import setup

setup(
    name='udp-chat',
    version='0.0.1',
    author='Zeke Zhang',
    description='cli chat application using udp',
    scripts=['main.py'],
    entry_points={
        'console_scripts': [
            'udp-chat = main:main',
        ],
    },
)