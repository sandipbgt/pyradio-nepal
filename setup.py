#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
    
requirements = [pkg.split('=')[0] for pkg in open('requirements.txt').readlines()]

description = "Commandline tool to listen all radio stations of Nepal"

long_description = open("README.rst").read()

classifiers = ['Environment :: Console',
               'Programming Language :: Python :: 3'
               ]

version = open('CHANGES.txt').readlines()[0][1:].strip()

setup(name='pyradio-nepal',
      version=version,
      description=description,
      author='Sandip Bhagat',
      author_email='sandipbgt@gmail.com',
      url='https://github.com/sandipbgt/pyradio-nepal',
      scripts=['src/pyradio-nepal',],
      install_requires=requirements,
      long_description=long_description,
      packages=['pyradio_nepal', 'pyradio_nepal.libradio'],
      package_dir = {'pyradio_nepal': 'src/pyradio_nepal'},
      package_data = {'pyradio_nepal': ['data/.radio_stations_json']},
      classifiers=classifiers
    )