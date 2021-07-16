import numpy as np
import matplotlib.pyplot as plt
from mathipy import numeric_operations as ops
#from mathipy.math import _math
import mathipy.math

class Function:
    function_type = 'Undefined Type'
    function_part = {
        'roots'       : 'green',
        'y-intercept' :  'blue',
        'vertex'      :   'red',
        'asymptote'   :'purple',
        'axis'        : 'black',
        'area'        :'orange'
    }

    def __init__(self, f: callable, **kwargs):
        self.f = ops.vectorize(f)
        self.kwargs = kwargs

    def calculate_values(self, x):
        return self.f(x, **self.kwargs)

    def __call__(self, x):
        return self.calculate_values(x)

    def get_yint(self):
        try:
            return self(0)
        except (ValueError, ZeroDivisionError):
            return np.nan

    def plot(self, pos: int = 0, range: int = 5, **kwargs):
        x_min, x_max = pos - range, pos + range
        x = np.linspace(x_min, x_max, 1000)
        y = self.calculate_values(x)

        fig, ax = plt.subplots()
        plt.grid()

        height = ops.kwargsParser(kwargs, ('height', 'h'), 1)
        v_scale = kwargs.get('vertical_scale', 'relative')
        if v_scale == 'relative':
            y_min, y_max = mathipy.math.statistics.min(y) - height, mathipy.math.statistics.max(y) + height
        elif v_scale == 'absolute':
            y_min, y_max = - height / 2, height / 2

        plt.xlim(x_min, x_max)
        try:
            plt.ylim(y_min, y_max)
        except ValueError:
            plt.ylim(-3,3)
    
        self.plot_func(ax)

        integrate_range = kwargs.get('integrate', None)
        if integrate_range:
            x1 = np.linspace(integrate_range[0], integrate_range[1])
            y1 = self.calculate_values(x1)
            ax.fill_between(x1, y1, color= Function.function_part['area'], alpha=0.5)

        ax.hlines(0, x_min, x_max, color= Function.function_part['axis'], alpha= 0.5)
        ax.vlines(0, y_min, y_max, color= Function.function_part['axis'], alpha= 0.5)
        plt.xlabel('$x$')
        plt.ylabel('$y$')
        ax.plot(x, y)
        plt.show()

    def plot_func(self, ax):
        ax.scatter(0, self.get_yint(), color= Function.function_part['y-intercept'])

    def __repr__(self):
        return f'{self.function_type} Function'


def differential(f: callable, x: float, magnitude: int = 13):
    """
    The differential of a function, dy/dx is:
    dy / dx = lim of Δx -> 0 of Δy / Δx, where Δy = f(x + Δx) - f(x), 
    Since computers can't represent infintely small numbers
    the differential is computed relative to the magnitude parameter.
    """
    delta_x: float = 10 ** -magnitude
    dy = f(x + delta_x) - f(x)
    return dy / delta_x


@ops.vectorize
def to_radian(x: float) -> float:
    return x / 360 * mathipy.math._math.tau


@ops.vectorize
def to_degree(x: float) -> float:
    return x / mathipy.math._math.tau * 360
