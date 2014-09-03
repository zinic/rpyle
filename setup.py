# -*- coding: utf-8 -*-
import os
import sys

from setuptools import setup, find_packages


def read(relative):
    contents = open(relative, 'r').read()
    return [l for l in contents.split('\n') if l != '']


setup(
    name='rpyle',
    version=read('src/rpyle/VERSION')[0],
    description='',
    author='John Hopper',
    author_email='john.hopper@jpserver.net',
    url='https://github.com/zinic/rpyle',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Other Environment',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Cython',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Topic :: Utilities'
    ],
    scripts=['src/scripts/rpyle'],
    tests_require=read('./project/tests_require.txt'),
    install_requires=read('./project/install_requires.txt'),
    test_suite='nose.collector',
    zip_safe=False,
    include_package_data=True,
    packages=find_packages('src/'),
    package_dir={'': 'src'})
