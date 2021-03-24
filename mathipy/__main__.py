import mathipy as mpy
import sys
import json
import pathlib
import argparse

PATH = pathlib.Path(__file__).parent

with open(PATH / 'funcConfigs.json', 'r') as file:
    jsonFile  = json.load(file)
    functions = jsonFile['functions']
    constants = jsonFile['constants']


mpy_description = '''
MathiPy tools from command line\n
-------------------------------\n'''

mpy_description += '\nAvailable functions: \n'
for f, d in functions.items():
    s = f'   -{f}: {d}' + '\n'
    mpy_description += s

mpy_description += '\nConstants: \n'
for c in constants:
    mpy_description += f'   -{c}\n'

parser = argparse.ArgumentParser(
    prog='MathiPy',
    formatter_class= argparse.RawDescriptionHelpFormatter,
    description= mpy_description,
    add_help=True,
    epilog=''
)
parser.add_argument('f', 
    help='Function defined in MathiPy'
)
parser.add_argument(
    'x', 
    nargs='*',
    help='Argument passed to f parameter'
)
parser.add_argument(
    '-r', '--range',
    action='store_true',
    dest='range_input',
    help='If used and, x will be passed to range function and passed to f.'
)
parser.add_argument(
    '-k', '--kwargs',
    nargs='*',
    default=None,
    dest='passed_kwargs',
    help='Pass kwargs for function f'
)

def formatArgs(*args):
    #Format 'x' parameter if it's a list 
        x = []
        for arg in args:
            if arg in constants:
                arg = getattr(mpy, arg)
            elif arg == 'True' or arg == 'False':
                arg = arg == 'True'
            else:
                arg = complex(arg)
                if arg.imag == 0: 
                    arg = int(arg.real) if arg.real.is_integer() else arg.real
            x.append(arg)
        return x

def main(**kwargs):
        function = kwargs['f']
        f = getattr(mpy, function)

        args = kwargs['x']
        args = formatArgs(*args)
        
        if kwargs['range_input']:
            args = list(range(*args))

        if kwargs['passed_kwargs']:
            functionKwargs = kwargs['passed_kwargs']
            functionKwargs = formatArgs(*functionKwargs)
        else:
            functionKwargs = ()
        print(f(args, *functionKwargs))

if __name__ == '__main__':
    kwargs = parser.parse_args()
    main(**vars(kwargs))