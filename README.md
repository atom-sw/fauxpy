# FauxPy

[![PyPI version](https://badge.fury.io/py/fauxpy.svg)](https://badge.fury.io/py/fauxpy)
[![Downloads](https://static.pepy.tech/badge/fauxpy)](https://pepy.tech/project/fauxpy)
[![Documentation Status](https://readthedocs.org/projects/fauxpy/badge/?version=latest)](https://fauxpy.readthedocs.io/en/latest/?badge=latest)
[![FauxPy-Test - Repository](https://img.shields.io/badge/FauxPy--Test-Repository-2ea44f)](https://github.com/mohrez86/fauxpy-test)
![Research](https://img.shields.io/badge/Research-Driven-lightgrey)
![Open Source](https://img.shields.io/badge/Open%20Source-Yes-brightgreen)
[![GitHub](https://img.shields.io/github/license/atom-sw/fauxpy)](LICENSE)

## What is FauxPy?

FauxPy (pronounced: *foh pie*) is an **automated fault localization tool** for Python programs.  
It helps developers **locate the root cause of software bugs** using advanced **dynamic analysis techniques**.  

💡 *Help improve FauxPy! Share your feedback in our [Discussions](https://github.com/mohrez86/fauxpy/discussions).*

### Features

FauxPy supports **seven classic fault localization techniques** in four families:

1. **SBFL** (spectrum-based) techniques Tarantula, Ochiai, and DStar.
2. **MBFL** (mutation-based) techniques Metallaxis and Muse.
3. **PS** (predicate switching) fault localization.
4. **ST** (stack-trace) fault localization.

It supports fault localization at the
level of **statements** 
(statement-level granularity) and at
the level of **functions** 
(function-level granularity).

FauxPy is based on **dynamic analysis**, and works seamlessly with tests written in:

- [Pytest](https://pytest.org)  
- [Unittest](https://docs.python.org/3/library/unittest.html)  
- [Hypothesis](https://hypothesis.works/)

## Documentation  

Full documentation is available at
[FauxPy documentation](https://fauxpy.readthedocs.io/).  

## Installation

To install FauxPy, follow the instructions in the 
[Installation Guide](https://fauxpy.readthedocs.io/en/latest/user/install).

## Usage

For a quick example of how to use FauxPy, refer to the 
[Usage Example](https://fauxpy.readthedocs.io/en/latest/user/start).  

## How to Cite

If you use this tool in your research, please cite it as described in our citation guide:
[How to Cite](https://fauxpy.readthedocs.io/en/latest/user/citation/)

## Mirrors

This repository is a public mirror of 
(part of) FauxPy's private development 
repository. There are two public 
mirrors, whose content 
is identical:

- https://github.com/atom-sw/fauxpy
- https://github.com/mohrez86/fauxpy
