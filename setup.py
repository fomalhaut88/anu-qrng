from setuptools import setup, find_packages

from anu_qrng.version import __version__

setup(
    name='anu-qrng',
    version=__version__,
    description='A Python interface for QRNG service (https://qrng.anu.edu.au/)',
    author='Alex Fomalhaut',
    packages=find_packages(),
    install_requires=[
        'aiohttp==3.8.3',
        'requests==2.28.1',
    ],
)
