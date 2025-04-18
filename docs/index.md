# FauxPy Documentation

[![PyPI version](https://badge.fury.io/py/fauxpy.svg)](https://badge.fury.io/py/fauxpy)
[![Downloads](https://static.pepy.tech/badge/fauxpy)](https://pepy.tech/project/fauxpy)
![Research](https://img.shields.io/badge/Research-Driven-lightgrey)
[![Open Source](https://img.shields.io/badge/Open%20Source-Yes-brightgreen)](https://github.com/atom-sw/fauxpy)
[![GitHub](https://img.shields.io/github/license/atom-sw/fauxpy)](https://github.com/atom-sw/fauxpy/blob/main/LICENSE)
[![Tests](https://github.com/mohrez86/fauxpy/actions/workflows/test-all.yml/badge.svg)](https://github.com/mohrez86/fauxpy/actions/workflows/test-all.yml)

## What is FauxPy?

FauxPy (pronounced: *foh pie*) is an **automated fault localization tool** for Python programs.  
It helps developers **locate the root cause of software bugs** using advanced **dynamic analysis techniques**.

FauxPy is **open-source** and available on [GitHub](https://github.com/atom-sw/fauxpy).  
This documentation provides installation steps, usage instructions, and API details.

!!! tip "New in FauxPy: LLM-Driven MBFL 🚀"
    FauxPy now supports **LLM-Driven Mutation-Based Fault 
    Localization**!  
    This functionality is the result of 
    integrating [PyLLMut](https://pyllmut.readthedocs.io)
    into FauxPy.  
    Check out 
    [Example 2 on the Quick Start page](user/start.md#example-2)
    to see this new feature in action.

!!! Feedback  
    Help improve FauxPy! Share your feedback in our [Discussions](https://github.com/mohrez86/fauxpy/discussions).

---

## Features  

FauxPy supports **seven classic fault localization techniques** in four families:

1.  **SBFL** (spectrum-based) techniques Tarantula, Ochiai, and DStar.
2.  **MBFL** (mutation-based) techniques Metallaxis and Muse.
3.  **PS** (predicate switching) fault localization.
4.  **ST** (stack-trace) fault localization.

It supports fault localization at the level of **statements**
(statement-level granularity) and at the level of **functions**
(function-level granularity).

FauxPy is based on **dynamic analysis**, and works seamlessly with tests written in:

- [Pytest](https://pytest.org)  
- [Unittest](https://docs.python.org/3/library/unittest.html)  
- [Hypothesis](https://hypothesis.works/)

FauxPy can also leverage large language models (LLMs) to 
improve fault localization effectiveness.

---

## FauxPy in Action  

Watch this **demo video** to see FauxPy in action!  
It covers:

- Running FauxPy on real-world Python projects  
- Interpreting fault localization results  
- Best practices for debugging with FauxPy

[![Watch the Demo](https://img.youtube.com/vi/6ooPPiwd79g/0.jpg)](https://www.youtube.com/watch?v=6ooPPiwd79g)

![YouTube Video Views](https://img.shields.io/youtube/views/6ooPPiwd79g)

---

## Explore the Documentation  

- **[User Guide](user/install.md)** – Learn how to **install** and **use FauxPy** effectively.  
- **[API Reference](api/intro.md)** – Documentation of FauxPy’s **main entry point** and the **two core classes** that handle execution.

---
