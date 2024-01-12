from setuptools import setup

setup(
    name='udp-chat',
    version='0.0.5',
    author='Zeke Zhang',
    description='cli chat application using udp',
    scripts=['main.py'],
    entry_points={
        'console_scripts': [
            'udp-chat = main:main',
        ],
    },
)