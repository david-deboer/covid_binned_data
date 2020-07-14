#! /usr/bin/env python
# -*- mode: python; coding: utf-8 -*-
# Copyright 2019 David DeBoer
# Licensed under the 2-clause BSD license.

"""Berkeley Geo-Binned Covid-19 setup."""
from setuptools import setup
import glob

setup_args = {
    'name': "binc19",
    'description': "Geo-Binned Covid-19",
    'license': "BSD",
    'author': "David DeBoer",
    'author_email': "ddeboer@berkeley.edu",
    'version': '0.1',
    'packages': ['binc19'],
    'scripts': glob.glob('scripts/*'),
    'include_package_data': True,
    'install_requires': []
}

if __name__ == '__main__':
    setup(**setup_args)
