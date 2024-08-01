=============
Usage Example
=============

The
`examples <https://github.com/atom-sw/fauxpy/tree/main/examples>`_
directory in FauxPy's repository includes the ``triangle_area`` example,
a tutorial demonstrating how to use FauxPy.
Follow the instructions below to run FauxPy
with this example.

Triangle Area
=============

The following walkthrough starts by discussing
`Triangle Area <https://github.com/atom-sw/fauxpy/tree/main/examples/triangle_area>`_'s
project structure
and  provides instructions
on setting up an environment and running FauxPy.

Project Structure
-----------------

The current example has two packages: `code`_ and `tests`_.
The code package contains the project's source code, which are two Python
modules: `code/equilateral.py`_ and `code/isosceles.py`_,
demonstrated in Figures 1 and 2, respectively.
The function in module ``equilateral.py``
computes the area of an equilateral triangle
and the function in module ``isosceles.py`` computes
the area of an isosceles triangle.

.. code-block:: python
   :linenos:
   :emphasize-lines: 11
   :caption: Figure 1: equilateral.py

    import math


    def equilateral_area(a):
        const = math.sqrt(3) / 4

        if a == 1:
            return const

        term = math.pow(a, 2)
        area = const + term  # bug
        # area = const * term  # patch
        return area

.. code-block:: python
   :linenos:
   :emphasize-lines: 6
   :caption: Figure 2: isosceles.py

    import math


    def isosceles_area(leg, base):
        def height():
            t1, t2 = math.pow(base, 2), math.pow(leg, 2) / 4  # bug
            # t1, t2 = math.pow(leg, 2), math.pow(base, 2) / 4  # patch
            return math.sqrt(t1 - t2)

        area = 0.5 * base * height()
        return area

Both functions have a bug. The bug locations are marked with comment
``bug`` within source code and highlighted in Figures 1 and 2.
The patch for each bug is in the line
following the bug location, in the form of a comment.

The ``tests`` package contains the project's test suite, including two test modules
`tests/test_equilateral.py`_ (Figure 3) and
`tests/test_isosceles.py`_ (Figure 4)
for modules ``equilateral.py`` and ``isosceles.py``,
respectively. Each of these two test modules has two tests, one failing (i.e., revealing the bug) and
one passing on their corresponding modules in package ``code``.

.. code-block:: python
   :linenos:
   :caption: Figure 3: test_equilateral.py

    import math

    import pytest

    from code.equilateral import equilateral_area


    def test_ea_fail():
        a = 3
        area = equilateral_area(a)
        assert area == pytest.approx(9 * math.sqrt(3) / 4)


    def test_ea_pass():
        a = 1
        area = equilateral_area(a)
        assert area == pytest.approx(math.sqrt(3) / 4)

.. code-block:: python
   :linenos:
   :caption: Figure 4: test_isosceles.py

    import math

    import pytest

    from code.isosceles import isosceles_area


    def test_ia_crash():
        leg, base = 9, 4

        area = isosceles_area(leg, base)
        assert area == pytest.approx(2 * math.sqrt(77))


    def test_ia_pass():
        leg = base = 4

        area = isosceles_area(leg, base)
        assert area == pytest.approx(2 * math.sqrt(12))

.. _code: https://github.com/atom-sw/fauxpy/tree/main/examples/triangle_area/code
.. _tests: https://github.com/atom-sw/fauxpy/tree/main/examples/triangle_area/tests
.. _code/equilateral.py: https://github.com/atom-sw/fauxpy/blob/main/examples/triangle_area/code/equilateral.py
.. _code/isosceles.py: https://github.com/atom-sw/fauxpy/blob/main/examples/triangle_area/code/isosceles.py
.. _tests/test_equilateral.py: https://github.com/atom-sw/fauxpy/blob/main/examples/triangle_area/tests/test_equilateral.py
.. _tests/test_isosceles.py: https://github.com/atom-sw/fauxpy/blob/main/examples/triangle_area/tests/test_isosceles.py

Preparing the Python Environment
--------------------------------

To follow this walkthrough on your machine,
first clone
`FauxPy's repository <https://github.com/atom-sw/fauxpy>`_
and navigate to
the ``triangle_area`` directory:

.. code-block:: bash

   git clone git@github.com:atom-sw/fauxpy.git
   cd fauxpy/examples/triangle_area

Then, create a Python environment for this
project, following the
instructions below.

1. Create a Python 3.8 virtual
   environment ``env``. More recent
   Python versions should also work.

.. code-block:: bash

   python3.8 -m venv env

2. Activate environment ``env``. Henceforth, all commands assume
   environment ``env`` is activated.

.. code-block:: bash

   source env/bin/activate

3. Install FauxPy in environment ``env``.

.. code-block:: bash

   pip install fauxpy

Locating the Bug in ``equilateral.py``
--------------------------------------

FauxPy is a Pytest plugin, and thus, running it
is similar to running Pytest.
Let's first use Pytest to run all the
tests in package ``tests``.

.. code-block:: bash

   python -m pytest tests

Running the command prints the following message, indicating there
are 4 tests in the project, 2 of which are failing.

.. code-block::

   2 failed, 2 passed in 0.07s

Running Spectrum-Based Fault Localization (SBFL)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Now let's run FauxPy.
FauxPy has only one mandatory command line option
``--src``, which takes a package (directory)
or module (``.py`` file) in the current project.
Since the source code of our project is in package ``code``,
we pass ``code`` to ``--src``.

.. code-block:: bash

   python -m pytest tests --src code

By default, FauxPy runs SBFL (spectrum-based fault localization). The
command finishes quickly, printing three lists, one for each SBFL
technique currently supported by FauxPy: Tarantula, Ochiai, and DStar.

The list for Tarantula looks something like
the following. Each row in this list
shows a line number in package ``code``
and a number (e.g., 1.1) denoting the line's suspiciousness score
according to Tarantula.

The location of the bug in ``equilateral.py`` is ``equilateral.py::11``,
and the location of the bug in ``isosceles.py`` is ``isosceles.py::6``.
Thus, Tarantula detected the locations of both bugs.

.. code-block::

   ('~/fauxpy-examples-dev/triangle_area/code/equilateral.py::13', 1.1)
   ('~/fauxpy-examples-dev/triangle_area/code/equilateral.py::11', 1.1)
   ('~/fauxpy-examples-dev/triangle_area/code/equilateral.py::10', 1.1)
   ('~/fauxpy-examples-dev/triangle_area/code/isosceles.py::8', 0.6)
   ('~/fauxpy-examples-dev/triangle_area/code/isosceles.py::6', 0.6)
   ('~/fauxpy-examples-dev/triangle_area/code/isosceles.py::5', 0.6)
   ('~/fauxpy-examples-dev/triangle_area/code/isosceles.py::10', 0.6)
   ('~/fauxpy-examples-dev/triangle_area/code/equilateral.py::7', 0.6)
   ('~/fauxpy-examples-dev/triangle_area/code/equilateral.py::5', 0.6)
   ('~/fauxpy-examples-dev/triangle_area/code/isosceles.py::11', 0.1)
   ('~/fauxpy-examples-dev/triangle_area/code/equilateral.py::8', 0.1)

While we just used FauxPy
to localize multiple bugs in one go,
it is normally preferable to analyze each bug separately from the others.
In FauxPy, we can do this in two ways:

1. Selecting tests

2. Selecting failing tests

Selecting Tests
"""""""""""""""

The following command runs FauxPy
using only the tests in ``tests/test_equilateral.py``.
Since the failing test in ``tests/test_equilateral.py``
is related to only a single bug,
FauxPy only localizes that one bug.

.. code-block:: bash

   python -m pytest tests/test_equilateral.py --src code

Tarantula's output list is now as follows, including only lines in
``equilateral.py``.

.. code-block::

   ('~/fauxpy-examples-dev/triangle_area/code/equilateral.py::13', 1.1)
   ('~/fauxpy-examples-dev/triangle_area/code/equilateral.py::11', 1.1)
   ('~/fauxpy-examples-dev/triangle_area/code/equilateral.py::10', 1.1)
   ('~/fauxpy-examples-dev/triangle_area/code/equilateral.py::7', 0.6)
   ('~/fauxpy-examples-dev/triangle_area/code/equilateral.py::5', 0.6)
   ('~/fauxpy-examples-dev/triangle_area/code/equilateral.py::8', 0.1)

Selecting Failing Tests
"""""""""""""""""""""""

The following command runs FauxPy using the whole test suite ``tests``
but **only** one *failing* test
``tests/test_equilateral.py::test_ea_fail``, which triggers the bug in
``equilateral.py``.

.. code-block:: bash

   python -m pytest tests --src code --failing-list "[tests/test_equilateral.py::test_ea_fail]"

Tarantula's output list is now as follows, including lines from any files but
correctly ranking line ``equilateral.py::11`` in the top suspiciousness position.

.. code-block::

   ('~/fauxpy-examples-dev/triangle_area/code/equilateral.py::13', 1.1)
   ('~/fauxpy-examples-dev/triangle_area/code/equilateral.py::11', 1.1)
   ('~/fauxpy-examples-dev/triangle_area/code/equilateral.py::10', 1.1)
   ('~/fauxpy-examples-dev/triangle_area/code/equilateral.py::7', 0.75625)
   ('~/fauxpy-examples-dev/triangle_area/code/equilateral.py::5', 0.75625)
   ('~/fauxpy-examples-dev/triangle_area/code/isosceles.py::8', 0.1)
   ('~/fauxpy-examples-dev/triangle_area/code/isosceles.py::6', 0.1)
   ('~/fauxpy-examples-dev/triangle_area/code/isosceles.py::5', 0.1)
   ('~/fauxpy-examples-dev/triangle_area/code/isosceles.py::11', 0.1)
   ('~/fauxpy-examples-dev/triangle_area/code/isosceles.py::10', 0.1)
   ('~/fauxpy-examples-dev/triangle_area/code/equilateral.py::8', 0.1)

As you can see, both approaches report the bug line in
``equilateral.py`` as the second element in the output list, tied with
two other lines in the same file. Note that the order of lines with the same suspiciousness score is immaterial; thus, a user would have to go through all three lines to determine if one of them is indeed the correct fault location.

Running Mutation-Based Fault Localization (MBFL)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To run MBFL techniques, we pass option ``--family mbfl``.

.. code-block:: bash

   python -m pytest tests --src code --family mbfl --failing-list "[tests/test_equilateral.py::test_ea_fail]"

The command prints two lists, one for each MBFL
technique currently supported by FauxPy: Metallaxis and Muse.

The list for Muse looks something like the following.

.. code-block::

   ('~/fauxpy-examples-dev/triangle_area/code/equilateral.py::11', 0.09090909090909091)
   ('~/fauxpy-examples-dev/triangle_area/code/equilateral.py::10', 0.0)
   ('~/fauxpy-examples-dev/triangle_area/code/equilateral.py::7', -0.039660506068057426)
   ('~/fauxpy-examples-dev/triangle_area/code/equilateral.py::5', -0.055524708495280385)

Remember that ``equilateral.py::11`` is the actual bug location in ``equilateral.py``.
This line is ranked top, and all other lines have a strictly lower suspiciousness score. Thus, Muse localizes this bug perfectly.

Note that you cannot compare the value of suspiciousness scores
between techniques: what matters is the ranking of lines by
suspiciousness.

Running Stack Trace (ST) and Predicate Switching (PS) Fault Localization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To run the ST technique, we pass option ``--family st``.

.. code-block:: bash

   python -m pytest tests --src code --family st --failing-list "[tests/test_equilateral.py::test_ea_fail]"

And, to run the PS technique, we pass option ``--family ps``:

.. code-block:: bash

   python -m pytest tests --src code --family ps --failing-list "[tests/test_equilateral.py::test_ea_fail]"

Both techniques return an empty output list, which means that
they failed to localize the bug in ``equilateral.py``.

Locating the Bug in `isosceles.py`
----------------------------------

Now, let's run some of the techniques on the other bug in `isosceles.py`.

Here is how to run SBFL. Note that we changed the argument
``--failing-list``, so that we switch to `isosceles.py`'s bug.

.. code-block:: bash

   python -m pytest tests --src code --family sbfl --failing-list "[tests/test_isosceles.py::test_ia_crash]"

Tarantula's output list is as follows:

.. code-block::

   ('~/fauxpy-examples-dev/triangle_area/code/isosceles.py::8', 0.75625)
   ('~/fauxpy-examples-dev/triangle_area/code/isosceles.py::6', 0.75625)
   ('~/fauxpy-examples-dev/triangle_area/code/isosceles.py::5', 0.75625)
   ('~/fauxpy-examples-dev/triangle_area/code/isosceles.py::10', 0.75625)
   ('~/fauxpy-examples-dev/triangle_area/code/isosceles.py::11', 0.1)
   ('~/fauxpy-examples-dev/triangle_area/code/equilateral.py::8', 0.1)
   ('~/fauxpy-examples-dev/triangle_area/code/equilateral.py::7', 0.1)
   ('~/fauxpy-examples-dev/triangle_area/code/equilateral.py::5', 0.1)

Now we run MBFL:

.. code-block:: bash

   python -m pytest tests --src code --family mbfl --failing-list "[tests/test_isosceles.py::test_ia_crash]"

Metallaxis's output list is as follows:

.. code-block::

   ('~/fauxpy-examples-dev/triangle_area/code/isosceles.py::10', 0.5)
   ('~/fauxpy-examples-dev/triangle_area/code/isosceles.py::6', 0.5)
   ('~/fauxpy-examples-dev/triangle_area/code/isosceles.py::8', 0.5)

We could also run ST and PS by simply replacing ``mbfl`` with ``st`` or
``ps`` in the previous command. However, ST and PS only need failing
tests; rather than letting FauxPy run all tests and discover which
ones are failing, we can point it directly to only use a specific
failing test, which may save some time if our test suite includes many
passing tests (useless for ST and PS). To this end, we invoke FauxPy
as follows to run ST:

.. code-block:: bash

   python -m pytest tests/test_isosceles.py::test_ia_crash --src code --family st

Note that we no longer need option ``--failing-list``, since the test
suite we are using now contains one single failing test.

ST's output is as follows.

.. code-block::

   ('~/fauxpy-examples-dev/triangle_area/code/isosceles.py::height::5::8', 1.0)
   ('~/fauxpy-examples-dev/triangle_area/code/isosceles.py::isosceles_area::4::11', 0.5)

Each entry specifies a *range* of lines (such as from line ``5`` to line
``8`` in the top position). This is because ST cannot distinguish
between statements within the same function, and hence it will always
cluster function bodies together.

Similarly, we run PS with only the failing test as follows:

.. code-block:: bash

   python -m pytest tests/test_isosceles.py::test_ia_crash --src code --family ps

PS returns an empty list of lines on this example as well. PS can only
localize bugs that originate in branching predicates (such as
conditionals and loop exit conditions), and hence it is a poor match
for these examples.

Function-level Granularity
--------------------------

In all the examples seen so far, FauxPy ran with statement-level
granularity. This means that it localizes *lines* within a program.

FauxPy also supports function-level granularity; in this case, it
reports a list of *functions* within a program, each with a certain
suspiciousness score.

To run any of the previous examples with function-level
granularity, pass option ``--granularity function``, which overrides the
default ``--granularity statement``.

For instance, here is how to run SBFL with function-level granularity
on `isosceles.py`.

.. code-block:: bash

   python -m pytest tests --src code --family sbfl --granularity function --failing-list "[tests/test_isosceles.py::test_ia_crash]"

Tarantula's output list is as follows:

.. code-block::

   ('~/fauxpy-examples-dev/triangle_area/code/isosceles.py::isosceles_area::4::11', 0.75625)
   ('~/fauxpy-examples-dev/triangle_area/code/isosceles.py::height::5::8', 0.75625)
   ('~/fauxpy-examples-dev/triangle_area/code/equilateral.py::equilateral_area::4::13', 0.1)
