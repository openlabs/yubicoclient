# -*- coding: utf-8 -*-
"""
Yubico Client
-------------

The YubiKey generates a One-Time Passcode (OTP) that your application or 
service, ensuring that only users with a valid YubiKey can gain 
access. This api will help you to validate a OTP thus obtained against a yubico
server. Also supports custom Yubikey validation servers in addition to the 
default Yubico servers.

Its easy
````````

::
    from yubicoclient import YubicoClient
    client = YubicoClient(<client id>, <key>)
    client.verify(<OTP>)


To Install
``````````

::

    $ pip install yubicoclient
    (or)
    $ easy_install yubicoclient

Links
`````
  * `yubico <http://http://www.yubico.com//>`_
  * `API Documentation <http://code.google.com/p/yubikey-val-server-php/wiki/ValidationProtocolV20>`_
  * `Source Code <https://bitbucket.org/sharoonthomas/yubicoclient>`_

:copyright: © 2011 by Openlabs Technologies & Consulting (P) Limited
:license: BSD, see LICENSE for more details.
"""
from setuptools import setup

__version__ = '0.2.0'
__author__ = 'Sharoon Thomas, Openlabs Technologies & Consulting (P) Limited'

setup(
    name='yubicoclient',
    version=__version__,
    url='http://www.openlabs.co.in/',
    license='BSD',
    author='Sharoon Thomas, Openlabs Technologies & Consulting (P) Limited',
    description='Python yubico client',
    long_description=__doc__,
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
