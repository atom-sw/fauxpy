import os

from fauxpy.session_lib.path_lib import FauxpyPath


def test_path_lib_from_relative():
    pwd = "/home/user"
    rel = "a/b/c.py"
    fauxpy_path = FauxpyPath.from_relative_path(pwd, rel)
    assert fauxpy_path.get_relative() == "a/b/c.py"
    assert fauxpy_path.get_absolute() == "/home/user/a/b/c.py"

    pwd = "/home/user/"
    rel = "a/b/c.py"
    fauxpy_path = FauxpyPath.from_relative_path(pwd, rel)
    assert fauxpy_path.get_relative() == "a/b/c.py"
    assert fauxpy_path.get_absolute() == "/home/user/a/b/c.py"

    pwd = "/home/user"
    rel = "./a/b/c.py"
    fauxpy_path = FauxpyPath.from_relative_path(pwd, rel)
    assert fauxpy_path.get_relative() == "a/b/c.py"
    assert fauxpy_path.get_absolute() == "/home/user/a/b/c.py"

    pwd = "/home/user/././"
    rel = "a/b/c.py"
    fauxpy_path = FauxpyPath.from_relative_path(pwd, rel)
    assert fauxpy_path.get_relative() == "a/b/c.py"
    assert fauxpy_path.get_absolute() == "/home/user/a/b/c.py"

    pwd = "/home/user"
    rel = "./././././a/b/c.py"
    fauxpy_path = FauxpyPath.from_relative_path(pwd, rel)
    assert fauxpy_path.get_relative() == "a/b/c.py"
    assert fauxpy_path.get_absolute() == "/home/user/a/b/c.py"


def test_path_lib_from_absolute():
    absolute_path = "/home/user/a/b/c.py"
    pwd = "/home/user"
    fauxpy_path = FauxpyPath.from_absolute_path(pwd, absolute_path)
    assert fauxpy_path.get_relative() == "a/b/c.py"
    assert fauxpy_path.get_absolute() == "/home/user/a/b/c.py"

    absolute_path = "/home/././././user/a/b/c.py"
    pwd = "/home/user"
    fauxpy_path = FauxpyPath.from_absolute_path(pwd, absolute_path)
    assert fauxpy_path.get_relative() == "a/b/c.py"
    assert fauxpy_path.get_absolute() == "/home/user/a/b/c.py"

    absolute_path = "/home/user/a/b/c.py"
    pwd = "/home/user/"
    fauxpy_path = FauxpyPath.from_absolute_path(pwd, absolute_path)
    assert fauxpy_path.get_relative() == "a/b/c.py"
    assert fauxpy_path.get_absolute() == "/home/user/a/b/c.py"

    absolute_path = "/home/user/a/b/c.py"
    pwd = "/home/user/./././././."
    fauxpy_path = FauxpyPath.from_absolute_path(pwd, absolute_path)
    assert fauxpy_path.get_relative() == "a/b/c.py"
    assert fauxpy_path.get_absolute() == "/home/user/a/b/c.py"


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
