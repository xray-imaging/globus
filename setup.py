from setuptools import setup, find_packages
from setuptools.command.install import install
import os


setup(
    name='globus',
    version=open('VERSION').read().strip(),
    #version=__version__,
    author='Francesco De Carlo',
    author_email='decarlof@gmail.com',
    url='https://github.com/xray-imaging/globus',
    packages=find_packages(),
    include_package_data = True,
    scripts=['bin/globus'],
    description='cli to run globus at 2-bm',
    zip_safe=False,
)