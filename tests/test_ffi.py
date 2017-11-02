import pytest

from file import MAGIC_NONE, magic_setflags, MAGIC_MIME, MAGIC_MIME_TYPE
from file import magic_buffer
from file import magic_file
from file import magic_load
from file import magic_open, magic_close
from file import magic_version


def test_version():
    version = magic_version()
    assert isinstance(version, int)


def test_open():
    cookie = magic_open(MAGIC_NONE)
    assert cookie is not None


def test_close():
    cookie = magic_open(MAGIC_NONE)
    assert cookie is not None
    magic_close(cookie)


def test_load():
    cookie = magic_open(MAGIC_NONE)
    assert cookie is not None
    with pytest.raises(ValueError):
        magic_load(cookie, b"/etc/magic_database")
    magic_load(cookie)


def test_file():
    cookie = magic_open(MAGIC_NONE)
    assert cookie is not None

    magic_load(cookie)
    mimetype = magic_file(cookie, b"/etc/passwd")
    assert mimetype == b"ASCII text"


def test_buffer():
    cookie = magic_open(MAGIC_NONE)
    assert cookie is not None
    magic_load(cookie)

    mimetype = magic_buffer(cookie, b"")
    assert mimetype == b"empty"

    mimetype = magic_buffer(cookie, b"kittens")
    assert mimetype == b"ASCII text, with no line terminators"

    mimetype = magic_buffer(cookie, b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A")
    assert mimetype == b"PNG image data"


def test_set_flags():
    cookie = magic_open(MAGIC_NONE)
    assert cookie is not None

    magic_load(cookie)

    mimetype = magic_buffer(cookie, b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A")
    assert mimetype == b"PNG image data"

    magic_setflags(cookie, MAGIC_MIME_TYPE)
    mimetype = magic_buffer(cookie, b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A")
    assert mimetype == b"image/png"

    magic_setflags(cookie, MAGIC_MIME)
    mimetype = magic_buffer(cookie, b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A")
    assert mimetype == b"image/png; charset=binary"
