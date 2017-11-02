import pytest

from file import Magic, MAGIC_NONE


@pytest.fixture
def magic():
    with Magic(MAGIC_NONE) as magic:
        yield magic


def test_get_version(magic):
    assert isinstance(magic.version, int)


def test_from_buffer(magic):
    mimetype = magic.from_buffer("ehlo")
    assert mimetype == "ASCII text, with no line terminators"


def test_from_file(magic):
    mimetype = magic.from_file("/etc/passwd")
    assert mimetype == "ASCII text"


def test_with(magic):
    magic.set_flags(magic.flags.MAGIC_MIME_TYPE)
    mimetype = magic.from_file("/etc/passwd")
    assert mimetype == "text/plain"


def test_set_flags(magic):
    mimetype = magic.from_file("/etc/passwd")
    assert mimetype == "ASCII text"
    magic.set_flags(magic.flags.MAGIC_MIME_TYPE)
    mimetype = magic.from_file("/etc/passwd")
    assert mimetype == "text/plain"
