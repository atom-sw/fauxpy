import os

import pytest

from fauxpy.session_lib.fauxpy_path import FauxpyPath


def test_path_lib_from_relative_1():
    pwd = "/home/user"
    rel = "a/b/c.py"
    fauxpy_path = FauxpyPath.from_relative_path(pwd, rel)
    assert fauxpy_path.get_relative() == "a/b/c.py"
    assert fauxpy_path.get_absolute() == "/home/user/a/b/c.py"

def test_path_lib_from_relative_2():
    pwd = "/home/user/"
    rel = "a/b/c.py"
    fauxpy_path = FauxpyPath.from_relative_path(pwd, rel)
    assert fauxpy_path.get_relative() == "a/b/c.py"
    assert fauxpy_path.get_absolute() == "/home/user/a/b/c.py"

def test_path_lib_from_relative_3():
    pwd = "/home/user"
    rel = "./a/b/c.py"
    fauxpy_path = FauxpyPath.from_relative_path(pwd, rel)
    assert fauxpy_path.get_relative() == "a/b/c.py"
    assert fauxpy_path.get_absolute() == "/home/user/a/b/c.py"

def test_path_lib_from_relative_4():
    pwd = "/home/user/././"
    rel = "a/b/c.py"
    fauxpy_path = FauxpyPath.from_relative_path(pwd, rel)
    assert fauxpy_path.get_relative() == "a/b/c.py"
    assert fauxpy_path.get_absolute() == "/home/user/a/b/c.py"

def test_path_lib_from_relative_5():
    pwd = "/home/user"
    rel = "./././././a/b/c.py"
    fauxpy_path = FauxpyPath.from_relative_path(pwd, rel)
    assert fauxpy_path.get_relative() == "a/b/c.py"
    assert fauxpy_path.get_absolute() == "/home/user/a/b/c.py"

def test_path_lib_from_relative_6():
    pwd = "/home/user"
    rel = "."
    fauxpy_path = FauxpyPath.from_relative_path(pwd, rel)
    assert fauxpy_path.get_relative() == "."
    assert fauxpy_path.get_absolute() == "/home/user"

def test_path_lib_from_absolute_1():
    absolute_path = "/home/user/a/b/c.py"
    pwd = "/home/user"
    fauxpy_path = FauxpyPath.from_absolute_path(pwd, absolute_path)
    assert fauxpy_path.get_relative() == "a/b/c.py"
    assert fauxpy_path.get_absolute() == "/home/user/a/b/c.py"

def test_path_lib_from_absolute_2():
    absolute_path = "/home/././././user/a/b/c.py"
    pwd = "/home/user"
    fauxpy_path = FauxpyPath.from_absolute_path(pwd, absolute_path)
    assert fauxpy_path.get_relative() == "a/b/c.py"
    assert fauxpy_path.get_absolute() == "/home/user/a/b/c.py"

def test_path_lib_from_absolute_3():
    absolute_path = "/home/user/a/b/c.py"
    pwd = "/home/user/"
    fauxpy_path = FauxpyPath.from_absolute_path(pwd, absolute_path)
    assert fauxpy_path.get_relative() == "a/b/c.py"
    assert fauxpy_path.get_absolute() == "/home/user/a/b/c.py"

def test_path_lib_from_absolute_4():
    absolute_path = "/home/user/a/b/c.py"
    pwd = "/home/user/./././././."
    fauxpy_path = FauxpyPath.from_absolute_path(pwd, absolute_path)
    assert fauxpy_path.get_relative() == "a/b/c.py"
    assert fauxpy_path.get_absolute() == "/home/user/a/b/c.py"

def test_path_lib_from_absolute_5():
    absolute_path = "/home/user"
    pwd = "/home/user"
    fauxpy_path = FauxpyPath.from_absolute_path(pwd, absolute_path)
    assert fauxpy_path.get_relative() == "."
    assert fauxpy_path.get_absolute() == "/home/user"

def test_path_lib_changing_cwd():
    pwd = "/home/user"
    rel = "a/b/c.py"
    absolute_path = "/home/user/a/b/c.py"

    fauxpy_path = FauxpyPath.from_relative_path(pwd, rel)
    assert fauxpy_path.get_relative() == "a/b/c.py"
    assert fauxpy_path.get_absolute() == "/home/user/a/b/c.py"

    fauxpy_path = FauxpyPath.from_absolute_path(pwd, absolute_path)
    assert fauxpy_path.get_relative() == "a/b/c.py"
    assert fauxpy_path.get_absolute() == "/home/user/a/b/c.py"

    os.chdir("/")

    fauxpy_path = FauxpyPath.from_relative_path(pwd, rel)
    assert fauxpy_path.get_relative() == "a/b/c.py"
    assert fauxpy_path.get_absolute() == "/home/user/a/b/c.py"

    fauxpy_path = FauxpyPath.from_absolute_path(pwd, absolute_path)
    assert fauxpy_path.get_relative() == "a/b/c.py"
    assert fauxpy_path.get_absolute() == "/home/user/a/b/c.py"


def test_path_lib_dot_path():
    pwd = "/home/user"
    rel = "."
    fauxpy_path = FauxpyPath.from_relative_path(pwd, rel)
    assert fauxpy_path.get_relative() == "."
    assert fauxpy_path.get_absolute() == "/home/user"

def test_path_lib_using_constructor():
    with pytest.raises(NotImplementedError):
        FauxpyPath()
