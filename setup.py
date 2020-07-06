#!/usr/bin/env python3

from setuptools import setup, find_packages
from os import path, getcwd
from io import open

# Get current dir path
here = path.abspath(path.dirname(__file__))

# Get project name using project path
name = path.basename(getcwd())

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Get version from .VERSION file on the project root
with open(path.join(here, '.VERSION')) as version_file:
    version = version_file.read().strip()

# Get package requirements
with open(path.join(here, 'requirements.txt')) as f:
    requirements = f.read().splitlines()

setup(
    name=name,
    version=version,  # Required
    description='',  # Optional
    long_description=long_description,
    long_description_content_type='text/markdown',  # Optional (see note above)
    url='',
    author='Edouard DEVOUGE',  # Optional
    author_email='edevouge@gmail.com',  # Optional

    package_dir={'': 'src'},
    packages=find_packages(where='src'),  # Required
    python_requires='>=3.5',
    install_requires=requirements,  # Optional
    entry_points={  # Optional
        'console_scripts': [
            '{}={}:main'.format(name, name),
        ],
    },
)
