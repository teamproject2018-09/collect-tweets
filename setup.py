#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

setup(
    name='collect-tweets',
    version='0.1.0',
    description="collect-tweets",
    long_description=readme + '\n\n',
    author="Erik Tjong Kim Sang",
    author_email='e.tjongkimsang@esciencecenter.nl',
    url='https://github.com//collect-tweets',
    packages=[
        'collect-tweets',
    ],
    package_dir={'collect-tweets':
                 'collect-tweets'},
    include_package_data=True,
    license="Apache Software License 2.0",
    zip_safe=False,
    keywords='collect-tweets',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    install_requires=[],  # FIXME: add your package's dependencies to this list
    setup_requires=[
        # dependency for `python setup.py test`
        'pytest-runner',
        # dependencies for `python setup.py build_sphinx`
        'sphinx',
        'recommonmark'
    ],
    tests_require=[
        'pytest',
        'pytest-cov',
        'pycodestyle',
    ],
    extras_require={
        'dev':  ['prospector[with_pyroma]', 'yapf', 'isort'],
    }
)
