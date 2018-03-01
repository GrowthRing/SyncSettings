# -*- coding: utf-8 -*-

import sys
import os
import platform
from functools import wraps

if sys.version_info < (3,):
    from urllib import unquote
    from urllib import quote
else:
    from urllib.parse import unquote
    from urllib.parse import quote


def os_path(func):
    @wraps(func)
    def path_wrapper(*args, **kwargs):
        sep = '\\' if platform.system() == 'Windows' else '/'
        w = func(*args, **kwargs)

        return w.replace('/', sep).replace('\\', sep)

    return path_wrapper


def encode(path):
    path = path.replace('\\', '/')
    return quote(path, safe='')


@os_path
def decode(path):
    return unquote(path)


@os_path
def join(*paths):
    return os.path.join(*paths)


def exists(path, folder=False):
    is_valid = os.path.isdir(path) if folder else os.path.isfile(path)
    return os.path.exists(path) and is_valid
