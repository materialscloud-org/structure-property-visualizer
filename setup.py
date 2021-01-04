#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Set up structure-property-visualizer"""

from __future__ import absolute_import
from setuptools import setup

if __name__ == '__main__':
    # Provide static information in setup.json
    # such that it can be discovered automatically
    setup(
        packages=['detail', 'figure'],
        name='structure-property-visualizer',
        author='Leopold Talirz',
        author_email='info@materialscloud.org',
        description=
        'A template for Materials Cloud DISCOVER sections using bokeh server.',
        license='MIT',
        classifiers=['Programming Language :: Python'],
        version='0.2.0',
        install_requires=[
            'bokeh~=1.4.0',
            'jsmol-bokeh-extension~=0.2.1',
            'pandas~=0.24.2',
            'sqlalchemy~=1.3.0',
            'requests~=2.21.0',
        ],
        extras_require={'pre-commit': ['pre-commit~=2.2', 'pylint~=2.6.0']})
