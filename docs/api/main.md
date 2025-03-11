Module `main.py` is the main entry point for FauxPy, containing six
functions. The function `fauxpy_analysis_mode` is called when FauxPy
starts in Analysis Mode. This function creates an instance of the
`FauxpyAnalysisModeHandler` class, 
which manages the whole Analysis Mode.

The other five functions in `main.py` are Pytest hooks executed in
Pytest Mode. Module `main.py` instantiates a
`FauxpyPytestModeHandler` object as 
a global variable. These hooks call corresponding
methods in the object, delegating control of Pytest Mode to class
`FauxpyPytestModeHandler`.

Below are the details of these six functions in `main.py`.

::: fauxpy.main
