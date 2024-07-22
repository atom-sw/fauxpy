Limitations
-----------

The current version of FauxPy has a couple of known limitations:

1. The implementation of SBFL and MBFL uses
   `Coverage.py <https://coverage.readthedocs.io>`_ through its API to
   collect execution traces. Thus, FauxPy inherits any limitation of Coverage.py.

2. The implementation of ST does not work properly if Pytest's option
   ``--tb=native`` is enabled (as a command-line argument or in a
   ``pytest.ini`` file).

3. FauxPy is incompatible with Pytest plugin
   `pytest-sugar <https://pypi.org/project/pytest-sugar/>`_. If you
   want to use FauxPy, remove ``pytest-sugar`` from your Python
   environment.
