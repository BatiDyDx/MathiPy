import numpy as np
import matplotlib.pyplot as plt
from mathipy import _math, numeric_operations as ops


class Function(object):
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
        self.function = f

    def calculate_values(self, x):
        vfunc = np.vectorize(self.function)
        return vfunc(x)

    def __call__(self, x):
        return self.calculate_values(x)

    def get_yint(self):
        try:
            return self(0)
        except ValueError:
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
            y_min, y_max = ops.min(y) - height, ops.max(y) + height
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


@np.vectorize
def to_radian(x: float) -> float:
    return x / 360 * _math.tau


@np.vectorize
def to_degree(x: float) -> float:
    return x / _math.tau * 360
