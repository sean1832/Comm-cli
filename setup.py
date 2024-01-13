from setuptools import setup
import json

manifest = json.load(open('manifest.json', 'r'))

setup(
    name=manifest['name'],
    version=manifest['version'],
    author=manifest['author'],
    description=manifest['description'],
    url=manifest['url'],
    entry_points={
        'console_scripts': [
            'nx = nx.main:main',
        ],
    },
)