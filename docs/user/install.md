# Installation

## Prerequisites  

Ensure you have:

- Python **3.6 or later** installed  
- `pip` (latest version recommended)  

We mainly tested FauxPy with Python 3.6, 3.7, and 3.8, but it should
also work on later Python versions.

## Installing FauxPy

FauxPy is [available on PyPI](https://pypi.org/project/fauxpy/). Install it via `pip`:

``` bash
pip install fauxpy
```

Or, to install the **latest development version** from GitHub:

``` bash
pip install git+https://github.com/atom-sw/fauxpy
```

Running this second command installs the latest version
of FauxPy available on the main branch of
[its GitHub repository](https://github.com/atom-sw/fauxpy).

## Setting Up Your LLM API Key

If you are using MBFL with mutation strategies beyond the traditional 
approach—i.e., those leveraging LLMs—you must 
configure an API key. This is because FauxPy relies on 
[PyLLMut](https://pyllmut.readthedocs.io/) 
to generate LLM-driven mutants, and PyLLMut requires 
an API key to access LLMs.

To set up your API key, follow the instructions in the 
[Setting Up Your LLM API Key](https://pyllmut.readthedocs.io/en/latest/user/install/#setting-up-your-llm-api-key) 
section of 
the PyLLMut installation guide.
