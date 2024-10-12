from pathlib import Path

import setuptools
from setuptools import setup


# Load version
root_path = Path(__file__).parent
version_file_path = root_path / "fauxpy" / "version.py"
__version__ = ""
exec(version_file_path.read_text())
assert __version__ != ""

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="fauxpy",
    version=__version__,
    author="Mohammad Rezaalipour",
    author_email="rezaalipour.mohammad@gmail.com",
    description="A fault localization tool for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/atom-sw/fauxpy",
    packages=setuptools.find_packages(exclude="tests"),
    python_requires=">=3.6",
    install_requires=[
        "pytest>=3.1.2",
        "coverage>=6.2",
        "cosmic-ray==8.3.5",
        "astor~=0.8.1",
        "pytest-timeout==2.1.0",
        "wheel",
    ],
    entry_points={
        "pytest11": [
            "fauxpy = fauxpy.main",
        ],
        "console_scripts": ["fauxpy = fauxpy.main:fauxpy_analysis_mode"],
    },
)
