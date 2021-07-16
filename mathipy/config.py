from ctypes import CDLL
import pathlib

###### Types ##########
from typing import Union

Real = Union[int, float]
Scalar = Union[int, float, complex]

########################

# Get the path to Mathipy
_mathipy_DIR = pathlib.Path(__file__).parent

def __path_to_cfuncs(_file_dir):
    """
    Returns the path to the cfuncs mathipy submodule, given the
    path of a file or subdirectory inside mathipy.
    If the directory passed is not a subdirectory of mathipy, 
    it raises a RuntimeError
    """
    PATH = pathlib.Path(_file_dir)
    
    # Checks if PATH is subdirectory of mathipy
    if PATH.is_relative_to(_mathipy_DIR):
        _C_PATH = PATH / 'cfuncs/bin/mpy_c_utils.so'
        return _C_PATH

    else:
        raise RuntimeError(f'{_file_dir} is not a subdirectory of {_mathipy_DIR}')

def __load_c_utils(_file_dir):
    """
    Given a file directory, it gets the path to cfuncs,
    loads it with CDLL, and returns it, so it is ready to
    use as an external module
    """
    return CDLL(__path_to_cfuncs(_file_dir))