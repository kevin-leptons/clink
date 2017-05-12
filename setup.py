#!/usr/bin/env python

'''
SYNOPSIS

    pip install -e .

DESCRIPTION

    Metadata for this package.

REFERENCES

    Building and Distributing Packages with Setuptools
        http://setuptools.readthedocs.io/en/latest/setuptools.html
'''

from setuptools import setup, find_packages


setup(
    name='clink',
    version='0.8.0',
    description='HTTP APIs Framework',
    keywords='http api framework',
    author='Kevin Leptons',
    author_email='kevin.leptons@gmail.com',
    url='https://github.com/kevin-leptons/clink',
    download_url='https://github.com/kevin-leptons/clink',
    python_requires=">=3.4",
    install_requires=[
        'pymongo==3.4.0'
    ],
    packages=find_packages(exclude=['tool', 'test']),
)
