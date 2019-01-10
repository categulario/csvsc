#!/usr/bin/env python3
from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst')) as f:
    long_description = f.read()

with open(path.join(here, 'csvsc', 'version.txt')) as f:
    version = f.read().strip()

setup(
    name='csvsc',
    description='Allows organization and redistribution of CSV data',
    long_description=long_description,
    url='https://github.com/categulario/csvsc',

    version=version,

    author='Abraham Toriz Cruz',
    author_email='categulario@gmail.com',
    license='MIT',

    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='csv, organization',

    packages=[
        'csvsc',
    ],

    package_data={
        'csvsc': ['version.txt'],
    },

    entry_points={
        'console_scripts': [
            'csvsc = csvsc.main:main',
        ],
    },

    install_requires=[
    ],

    setup_requires=[
        'pytest-runner',
    ],

    tests_require=[
        'pytest',
        'pytest-mock',
    ],
)
