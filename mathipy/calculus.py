import numpy as np
import matplotlib.pyplot as plt
import mathipy as mpy

class Function(object):
    function_part = {
        'roots'       : 'green',
        'y-intercept' :  'blue',
        'vertex'      :   'red',
        'asymptote'   :'orange',
        'axis'        : 'black',
        'area'        :'purple'
    }

    def __init__(self, f: callable, **kwargs):
        self.function = f

    def calculate_values(self, x: (int, iter)):
        if mpy.is_scalar(x):
            return self.function(x)
        else:
            return list(map(self.function, x))

    def __call__(self, x):
        return self.calculate_values(x)

    def get_yint(self):
        try:
            return self(0)
        except ValueError:
            return None

    def plot(self, pos= 0, rnge= 5, **kwargs):
        x_min, x_max = pos - rnge, pos + rnge
        x = np.linspace(x_min, x_max, 1000)
        y = self.calculate_values(x)

        fig, ax = plt.subplots()
        #plt.style.use('classic')
        plt.grid()

        height = kwargs.get('h', 1)
        v_scale = kwargs.get('vertical_scale', 'relative')
        if v_scale == 'relative':
            y_min, y_max = mpy.min(y) - height, mpy.max(y) + height
        elif v_scale == 'absolute':
            y_min, y_max = - height / 2, height / 2

        plt.xlim(x_min, x_max)
        try:
            plt.ylim(y_min, y_max)
        except ValueError:
            plt.ylim(-3,3)
    
        self.plot_func(ax)

        ax.hlines(0, x_min, x_max, color = Function.function_part['axis'], alpha = 0.5)
        ax.vlines(0, y_min, y_max, color = Function.function_part['axis'], alpha = 0.5)
        plt.xlabel('$x$')
        plt.ylabel('$y$')
        ax.plot(x, y)
        plt.show()

    def plot_func(self, ax):
        y_int = self.get_yint()
        ax.scatter(0, y_int, color = Function.function_part['y-intercept'])

    def integral(self):
        #TODO integral
        x1 = np.linspace(pos - 2, pos + 3, 1000)
        y1 = self.calculate_values(x1)
        ax.fill_between(x1, y1, color='red', alpha=0.5)
    
    def derivative(self):
        pass

class Derivative(object):
    """
    Derivative object for Function type objects
    """
    pass

class Integral(object):
    """
    Integral object for Function type objects
    """
    pass

def to_radian(x: float) -> float:
    return x / 360 * mpy.tau

def to_degree(x: float) -> float:
    return x / mpy.tau * 360