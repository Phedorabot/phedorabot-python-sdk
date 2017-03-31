#!/usr/bin/env python
#
# Copyright 2017 Phedorabot
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import os
import platform
import sys
import warnings

try:
    # Use setuptools if available, for install_requires (among other things).
    import setuptools
    from setuptools import setup
except ImportError:
    setuptools = None
    from distutils.core import setup

from distutils.core import Extension

from distutils.command.build_ext import build_ext

kwargs = {}

version = "1.0.0"

with open('README.md') as f:
    kwargs['long_description'] = f.read()

if setuptools is not None:
    # If setuptools is not available, you're on your own for dependencies.
    install_requires = ['requests','pyjwt']
    kwargs['install_requires'] = install_requires

setup(
    name="phedorabot",
    version=version,
    packages = ["phedorabot", "phedorabot.test"],
    package_data = {

        },
    author="Christian Amaonwu",
    author_email="amakris24@gmail.com",
    url="https://www.phedorabot.com/",
    license="http://www.apache.org/licenses/LICENSE-2.0",
    description="Phedorabot Python SDK",
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        ],
    **kwargs
)
