from setuptools import find_packages, setup

setup(
    name='nx',
    version='0.0.8',
    package_dir={'': 'nx'},
    packages=find_packages(where='nx'),
    author='Zeke Zhang',
    description='Simple local network data transfer CLI. Supports file transfer (udp and tcp) and text transfer.',
    entry_points={
        'console_scripts': [
            'nx = nx.main:main',
        ],
    },
)