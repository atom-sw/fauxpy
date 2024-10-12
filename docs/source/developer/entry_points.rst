=========================
Entry Points and Handlers
=========================

FauxPy can work in two different modes: **Pytest Mode** and **Analysis Mode**.

- **Pytest Mode** is activated when FauxPy is used with commands like
  ``pytest tests --src my_code``. In this mode, FauxPy runs as a Pytest
  plugin, integrating itself into the test execution pipeline to gather
  information about the tests being run.

- **Analysis Mode** is activated when FauxPy is used with commands like
  ``fauxpy -v``. In this mode, FauxPy runs as a standalone application,
  independently of Pytest.

Module ``main.py`` is the main entry point for FauxPy, determining
FauxPy's mode based on how FauxPy is executed.

Module ``main.py``
==================

This module is the main entry point for FauxPy, containing six functions.
The function ``fauxpy_analysis_mode`` is called when FauxPy starts in Analysis Mode.
It creates an instance of the ``FauxpyAnalysisModeHandler`` class, which manages
the whole Analysis Mode.

The other five functions in ``main.py`` are Pytest hooks executed in Pytest Mode.
Module ``main.py`` instantiates a ``FauxpyPytestModeHandler`` object as a global variable.
These hooks call corresponding methods in the object, delegating control
of Pytest Mode to class ``FauxpyPytestModeHandler``.

Below are the details of these six functions in ``main.py``.

.. automodule:: fauxpy.main
    :members:

Pytest Mode Handler
===================

Class ``FauxpyPytestModeHandler`` is responsible for managing Pytest Mode.
Details of this class are provided below.

.. automodule:: fauxpy.command_line.pytest_mode.handler
    :members:

Analysis Mode Handler
=====================

Class ``FauxpyAnalysisModeHandler`` manages Analysis Mode.
Details of this class are provided below. Currently, Analysis Mode
supports only one command, ``fauxpy --version``, which shows
the current version of FauxPy.

.. automodule:: fauxpy.command_line.analysis_mode.handler
    :members:
