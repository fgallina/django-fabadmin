#!/usr/bin/env python
# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name='django-fabadmin',
    version='0.0.1',
    description='Fabric Administration for Django.',
    author='Fabián E. Gallina',
    author_email='fabian@anue.biz',
    long_description=open('README.rst', 'r').read(),
    url='http://www.anue.biz',
    packages=['fabadmin'],
    package_data={},
    requires=['ansi2html'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities'
    ],
)
