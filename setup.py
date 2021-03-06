# -*- coding: utf-8 -*-
"""Installer for this package."""

from setuptools import setup

import os


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = \
    read('README.rst') + \
    read('docs', 'HISTORY.rst') + \
    read('docs', 'LICENSE')

setup(
    name='opensezame',
    version="0.1",
    description="HTTP server with trigger for ex. opening doors.",
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
    ],
    keywords='HTTP server',
    author='Matej Cotman',
    author_email='matejc@kiberpipa.org',
    url='https://github.com/matejc/opensezame',
    license='GNU GPL',
    packages=['opensezame'],
    package_dir={'opensezame': 'src/opensezame'},
    include_package_data=True,
    package_data={
        'opensezame': [
            'example/opensezame.json',
            'example/plugins/*.py',
            'example/templates/*/*.html'
        ]
    },
    zip_safe=False,
    install_requires=[
        'setuptools',
    ],
    extras_require={
        # list libs needed for unittesting this project
        'test': [
            'mock',
            'unittest2',
        ],
    },
    entry_points={
        'console_scripts': [
            "opensezame-run = opensezame:main",
            "opensezame-init = opensezame.entrypoints:init"
        ]
    },
)
