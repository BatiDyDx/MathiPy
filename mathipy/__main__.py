import mathipy as mpy
import json
import pathlib
import argparse

PATH = pathlib.Path(__file__)
mpy_PATH = PATH.parent

# Open CLI.json as read mode
with open(mpy_PATH / 'CLI.json', 'r') as file:
    jsonFile  = json.load(file)
    functions = jsonFile['functions']
    constants = jsonFile['constants']


mpy_description = '''
MathiPy tools from command line\n
-------------------------------\n'''

mpy_description += '\nAvailable functions: \n'
# Iterates over all functions defined in CLI.json
for f, d in functions.items():
    # Assign to s a string with the function name
    # and info to the description
    s = f'   -{f}: {d}' + '\n'
    mpy_description += s

mpy_description += '\nConstants: \n'
# Iterates over all constants defined in CLI
for c in constants:
    # Add the constant to the mathipy description
    mpy_description += f'   -{c}\n'

# Instantiate the ArgumentParser object, which includes
# the description, the programme name, etc.
parser = argparse.ArgumentParser(
    prog='MathiPy',
    formatter_class= argparse.RawDescriptionHelpFormatter,
    description= mpy_description,
    add_help=True,
    epilog=''
)

# The argument for the function to compute is added
parser.add_argument('f', 
    help='Function defined in MathiPy'
)

# The argument for x is added
parser.add_argument(
    'x', 
    nargs='*',
    help='Argument passed to f parameter'
)

# A range parameter is added, which, when used,
# creates a range object and passes it into f
parser.add_argument(
    '-r', '--range',
    action='store_true',
    dest='range_input',
    help='When used, evaluates f on range(x)'
)

# Adds an argument of undefined length, which will 
# contain the kwargs to be passed into f
parser.add_argument(
    '-k', '--kwargs',
    nargs='*',
    default=None,
    dest='keyboard_arguments',
    help='Pass kwargs for function f'
)

def formatArgs(*args):
    """
    Since arguemnts from the command line are strings,
    formatArgs assigns the corresponding value, in order
    to be correctly evaluated afterwards

    formatArgs('10', '1+2j', 'pi', 'False') = [10, 1+2j, 3.141592653589793, False]
    """
    #Format 'x' parameter if it's a list 
    x = []
    for arg in args:
        
        # If the argument is a constant available
        # it assigns to it the value of the constant 
        if arg in constants:
            arg = getattr(mpy, arg)
        
        # Assings True (resp. False) if the string is equal to 'True' (resp. 'False')
        elif arg == 'True' or arg == 'False':
            arg = arg == 'True'
        
        else:
            # Take arg as a complex number
            arg = complex(arg)
            if arg.imag == 0: 
                # If its imaginary part is 0, try to turn it into an int
                # else, keep it as a float
                # The reason for trying to cast it to an int is because of
                # some function parameters required to be integers 
                arg = int(arg.real) if arg.real.is_integer() else arg.real
        
        x.append(arg)

    return x

def main(**kwargs):
    # Get the function to be executed from the mathipy standard functions
    function = kwargs['f']
    f = getattr(mpy, function)

    # Convert the arguments passed to the function in the correct type
    args = kwargs['x']
    args = formatArgs(*args)
    
    # If the -r or --range argument is passed, the argument
    # passed to f will be a range of ints
    if kwargs['range_input']:
        args = list(range(*args))

    # Format the kwargs if any, to be passed to f
    if kwargs['keyboard_arguments']:
        functionKwargs = kwargs['keyboard_arguments']
        functionKwargs = formatArgs(*functionKwargs)
    # If no kwargs are passed, functionKwargs is an empty tuple
    else:
        functionKwargs = ()
    # Print to console the result of f evaluated with the passed args and kwargs
    print(f(args, *functionKwargs))

if __name__ == '__main__':
    parsed_kwargs = parser.parse_args()
    # Convert the parsed arguments into a dictionary
    kwargs = vars(parsed_kwargs)
    main(**kwargs)