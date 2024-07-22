FauxPy's documentation!
=======================


.. image:: https://badge.fury.io/py/fauxpy.svg
   :target: https://badge.fury.io/py/fauxpy

.. image:: https://img.shields.io/github/license/atom-sw/fauxpy
.. image:: https://static.pepy.tech/badge/fauxpy
   :target: https://pepy.tech/project/fauxpy

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black

FauxPy (pronounced: "foh pie") is an automated fault localization tool for Python programs,
`available as open-source software on GitHub <https://github.com/atom-sw/fauxpy>`_.
This documentation includes instructions to install and use FauxPy.

Features
--------

FauxPy supports seven classic fault-localization techniques in four families:

1. **SBFL** (spectrum-based) techniques Tarantula, Ochiai, and DStar.
2. **MBFL** (mutation-based) techniques Metallaxis and Muse.
3. **PS** (predicate switching) fault localization.
4. **ST** (stack-trace) fault localization.

It supports fault localization
at the level of **statements** (statement-level granularity)
and at the level of **functions** (function-level granularity).

FauxPy is based on dynamic analysis,
and can use tests written in the format of
`Pytest <https://pytest.org>`_,
`Unittest <https://docs.python.org/3/library/unittest.html>`_,
and `Hypothesis <https://hypothesis.works/>`_.

FauxPy in Action
----------------

Here is a short `demo video <https://www.youtube.com/watch?v=6ooPPiwd79g>`_
of FauxPy in action, presented by the developer of FauxPy at
`USI Università della Svizzera italiana <https://www.usi.ch/en>`_.

.. image:: https://img.youtube.com/vi/6ooPPiwd79g/0.jpg
   :target: https://www.youtube.com/watch?v=6ooPPiwd79g


Contents
--------

.. toctree::
   :maxdepth: 1

   user/installation
   user/getting_started
   user/using_fauxpy
   user/limitations
   user/citing_fauxpy_and_references
