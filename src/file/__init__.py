from . import ffi
from . import flags
from . import lib

__version__ = "0.1.0"


MAGIC_NONE = 0x000000  # No flags
MAGIC_DEBUG = 0x000001  # Turn on debugging
MAGIC_SYMLINK = 0x000002  # Follow symlinks
MAGIC_COMPRESS = 0x000004  # Check inside compressed files
MAGIC_DEVICES = 0x000008  # Look at the contents of devices
MAGIC_MIME_TYPE = 0x000010  # Return the MIME type
MAGIC_CONTINUE = 0x000020  # Return all matches
MAGIC_CHECK = 0x000040  # Print warnings to stderr
MAGIC_PRESERVE_ATIME = 0x000080  # Restore access time on exit
MAGIC_RAW = 0x000100  # Don't translate unprintable chars
MAGIC_ERROR = 0x000200  # Handle ENOENT etc as real errors
MAGIC_MIME_ENCODING = 0x000400  # Return the MIME encoding
MAGIC_MIME = (MAGIC_MIME_TYPE | MAGIC_MIME_ENCODING)
MAGIC_APPLE = 0x000800  # Return the Apple creator and type

MAGIC_NO_CHECK_COMPRESS = 0x001000  # Don't check for compressed files
MAGIC_NO_CHECK_TAR = 0x002000  # Don't check for tar files
MAGIC_NO_CHECK_SOFT = 0x004000  # Don't check magic entries
MAGIC_NO_CHECK_APPTYPE = 0x008000  # Don't check application type
MAGIC_NO_CHECK_ELF = 0x010000  # Don't check for elf details
MAGIC_NO_CHECK_TEXT = 0x020000  # Don't check for text files
MAGIC_NO_CHECK_CDF = 0x040000  # Don't check for cdf files
MAGIC_NO_CHECK_TOKENS = 0x100000  # Don't check tokens
MAGIC_NO_CHECK_ENCODING = 0x200000  # Don't check text encodings

MAGIC_NO_CHECK_FORTRAN = 0x000000  # Don't check ascii/fortran
MAGIC_NO_CHECK_TROFF = 0x000000  # Don't check ascii/troff


class Magic(object):
    def __init__(self, initial_flags=flags.MAGIC_MIME_TYPE, database=None):
        cookie = ffi.open(initial_flags)
        if database:
            ffi.load(cookie, database)
        else:
            ffi.load(cookie)
        self.cookie = cookie

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        ffi.close(self.cookie)

    @property
    def version(self):
        return ffi.version()

    def set_flags(self, flags):
        return ffi.set_flags(self.cookie, flags)

    def handle_bytes(function):
        def wrapper(self, value):
            if not isinstance(value, bytes):
                value = value.encode("utf-8")
            response = function(self, value)
            return response.decode("utf-8")

        return wrapper

    @handle_bytes
    def from_file(self, filepath):
        return ffi.file(self.cookie, filepath)

    @handle_bytes
    def from_buffer(self, value):
        return ffi.buffer(self.cookie, value)


def handle_null_exception(function):
    def wrapper(cookie, *args, **kwargs):
        response = function(cookie, *args, **kwargs)
        if response == ffi.NULL:
            message = error(cookie)
            raise ValueError(message)
        else:
            return ffi.string(response)

    return wrapper


def version():
    return lib.magic_version()


def set_flags(cookie, flags):
    status = lib.magic_setflags(cookie, flags)
    if status != 0:
        message = error(cookie)
        raise ValueError(message)
    else:
        return True


def error(cookie):
    message = lib.magic_error(cookie)
    return ffi.string(message)


def open(flags):
    cookie = lib.magic_open(flags)
    if cookie == ffi.NULL:
        message = error(cookie)
        raise RuntimeError(message)
    else:
        return cookie


def close(cookie):
    closed = lib.magic_close(cookie)
    return True


def load(cookie, path=ffi.NULL):
    status = lib.magic_load(cookie, path)
    if status != 0:
        message = error(cookie)
        raise ValueError(message)
    else:
        return True


@handle_null_exception
def file(cookie, path):
    mimetype = lib.magic_file(cookie, path)
    return mimetype


@handle_null_exception
def buffer(cookie, value):
    mimetype = lib.magic_buffer(cookie, value, len(value))
    return mimetype
