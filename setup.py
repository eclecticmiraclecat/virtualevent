# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in virtualevent/__init__.py
from virtualevent import __version__ as version

setup(
	name='virtualevent',
	version=version,
	description='VirtualEvent Portal',
	author='ERP-X',
	author_email='dev.erpx@gmail.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
