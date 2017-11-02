from . import ffi
from . import lib
from . import flags

__version__ = "0.4.0"


class Magic(object):

  def __init__(self, initial_flags=flags.MAGIC_MIME_TYPE, database=None):
    cookie = ffi.open(initial_flags)
    if database:
      ffi.load(cookie, database)
    else:
      ffi.load(cookie)
    self.cookie = cookie

  def __del__(self):
    try:
      ffi.close(self.cookie)
    except Exception as exception:
      raise

  def __enter__(self):
    return self

  def __exit__(self, type, value, traceback):
    del self

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
