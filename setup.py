# -*- coding: utf-8 -*-
"""

Youbico Yubikey Python client

:copyright: © 2011-2013 by Openlabs Technologies & Consulting (P) Limited
:license: BSD, see LICENSE for more details.
"""
from setuptools import setup

__version__ = '0.3.0'
__author__ = 'Sharoon Thomas, Openlabs Technologies & Consulting (P) Limited'

setup(
    name='yubicoclient',
    version=__version__,
    url='http://www.openlabs.co.in/',
    license='BSD',
    author='Sharoon Thomas, Openlabs Technologies & Consulting (P) Limited',
    description='Python yubico client',
    long_description=open('README.rst').read(),
    packages=['yubicoclient'],
    package_dir={
        'yubicoclient': '.'
        },
    platforms='any',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
