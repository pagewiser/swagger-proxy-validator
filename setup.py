#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import os
import sys
import re

if sys.argv[-1] == 'publish':
    os.system("python setup.py sdist upload")
    sys.exit()

base_dir = os.path.dirname(os.path.abspath(__file__))

def get_version(filename="SwaggerProxy/__init__.py"):
    with open(os.path.join(base_dir, filename)) as initfile:
        for line in initfile.readlines():
            m = re.match("__version__ *= *['\"](.*)['\"]", line)
            if m:
                return m.group(1)

setup(
    name = "swaggerproxy",
    version = get_version(),
    description = "Proxy server for API validation against Swagger documentation",
    packages = ['swaggerproxy'],
    dependency_links = ['https://github.com/marten-cz/flex/archive/new-features.tar.gz'],
    install_requires = [
        "requests >= 2.11.0",
        "swagger-parser >= 0.1.10",
        "swagger-spec-validator >= 2.0.2",
        "Twisted >= 16.0.0",
        "simplejson >= 3.8.0",
        "flex >= 5.9.0"  # Fixed some parts of the code, not yet merged
        ] + ["pypiwin32 >= 219"] if "win" in sys.platform else [],
    long_description=__doc__,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7'
    ]
)