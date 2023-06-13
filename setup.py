#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest-FauxPy',
    # name='fauxpy',
    packages=['fauxpy',
              'fauxpy.collect_mode',
              'fauxpy.common',
              'fauxpy.fauxpy_inst',
              'fauxpy.mbfl',
              'fauxpy.mbfl.mutgen',
              'fauxpy.predicate_switching',
              'fauxpy.predicate_switching.ast_manager',
              'fauxpy.program_tracer',
              'fauxpy.sbfl',
              'fauxpy.stack_trace'],
    version='0.1.0',
    author='AuthorFn AuthorLn',
    author_email='author@gmail.com',
    maintainer='AuthorFn AuthorLn',
    maintainer_email='author@gmail.com',
    license='MIT',
    url='https://github.com/author/pytest-pyafloc',
    description='Python automated fault localizer',
    long_description=read('README.md'),
    # py_modules=['pytest_pyafloc'],
    python_requires='>=3.5',
    install_requires=['pytest>=3.1.2',
                      'coverage>=6.2',
                      'cosmic-ray==8.3.5',
                      # 'cosmic-ray~=8.3.5',
                      # 'astor',
                      'astor~=0.8.1',
                      'pytest-timeout==2.1.0',
                      'wheel'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'pytest11': [
            'pytest-FauxPy = fauxpy.main',
        ],
    },
)
