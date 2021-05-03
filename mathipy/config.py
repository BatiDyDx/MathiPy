import ctypes
from ctypes import CDLL
import pathlib
from typing import TypeVar, Generic, Optional

_mathipy_DIR = pathlib.Path(__file__).parent

def __path_to_cfuncs(_file_dir):
    PATH = pathlib.Path(_file_dir)
    if PATH.is_relative_to(_mathipy_DIR):
        _C_PATH = PATH
        while _C_PATH.stem != 'mathipy':
            _C_PATH = _C_PATH.parent
    
    else:
        raise RuntimeError(f'{_file_dir} is not a subdirectory of {_mathipy_DIR}')
    
    _C_PATH /= 'cfuncs/bin/mpy_c_utils.so'
    return _C_PATH

def __load_c_utils(_file_dir):
    return CDLL(__path_to_cfuncs(_file_dir))