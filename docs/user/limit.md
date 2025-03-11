# Limitations  

The current version of FauxPy has a few known limitations:  

- **Dependency on Coverage.py**
    - FauxPy's **SBFL** and **MBFL** implementations use [Coverage.py](https://coverage.readthedocs.io) to collect execution traces.  
    - This means **any limitation of Coverage.py also applies to FauxPy**.  

- **Stack Trace (ST) Incompatibility with Pytest's `--tb=native`**  
    - FauxPy's **ST fault localization** does **not work correctly** if Pytest's `--tb=native` option is enabled.  
    - This option may be set **as a command-line argument** or in a `pytest.ini` file.  
    - **Solution:** Disable (remove) `--tb=native` when running FauxPy.  

- **Incompatibility with `pytest-sugar`**  
    - FauxPy **does not work with** the Pytest plugin [pytest-sugar](https://pypi.org/project/pytest-sugar/).  
    - **Solution:** Remove `pytest-sugar` from your Python environment before using FauxPy (e.g., `pip uninstall pytest-sugar`).
