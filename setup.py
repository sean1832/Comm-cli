from setuptools import setup, find_packages
import json

manifest = json.load(open('nx/manifest.json', 'r'))

setup(
    name=manifest['name'],
    version=manifest['version'],
    author=manifest['author'],
    description=manifest['description'],
    url=manifest['url'],
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '' : ['*.json']
    },
    entry_points={
        'console_scripts': [
            'nx = nx.main:main',
        ],
    },
)