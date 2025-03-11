# Entry Point and Handlers

FauxPy can work in two different modes: **Pytest Mode** and **Analysis
Mode**.

-   **Pytest Mode** is activated when FauxPy is used with commands like
    `pytest tests --src my_code`. In this mode, FauxPy runs as a Pytest
    plugin, integrating itself into the test execution pipeline to
    gather information about the tests being run.
-   **Analysis Mode** is activated when FauxPy is used with commands
    like `fauxpy -v`. In this mode, FauxPy runs as a standalone
    application, independently of Pytest.

Module `main.py` (see [Main Entry Point](main.md)) is the main entry point for FauxPy. It redirects
FauxPy's execution to the appropriate handler 
class, [FauxpyPytestModeHandler](pytest.md) or [FauxpyAnalysisModeHandler](analysis.md), 
depending on how
FauxPy has been executed.
