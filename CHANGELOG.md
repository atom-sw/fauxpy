# FauxPy Changelog

## Unreleased

- Extended the schema of the MBFL database to store PyLLMut results.
- Include mutation strategy in the report directory name.
- Change the format of the config and time files from plain text to JSON.
- Add support for LLM-driven mutation-based fault localization
  by integrating PyLLMut into FauxPy. This includes 
  the `--mutation` argument to specify the mutation 
  strategy for MBFL techniques.
- Refactor some modules and add docstrings.
- Improve help messages for command-line arguments.
- Add shorthand options `s` and `f` for `--granularity statement` and `--granularity function`.
- Revise and improve documentation content.
- Migrate documentation from Sphinx to MkDocs.


## FauxPy 0.2.0

- Add entry for Analysis Mode.
- Refactor code structure.
- Add input validation for command-line arguments.
- Improve the Read the Docs
documentation.
- Update the README files in the
root and triangle example 
directory.
- Add `version.py` file to manage FauxPy's versioning.


## FauxPy 0.1.1

- Remove tests depending on FauxPy.
- Add Read the Docs documentation.
- Fix a bug in ST.
- Adopt the black code style.
- Add Triangle area example.
- Update readme.

## FauxPy 0.1

- The first release.
