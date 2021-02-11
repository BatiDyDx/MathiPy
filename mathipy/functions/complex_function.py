import numpy as np
import matplotlib.pyplot as plt
from mathipy import calculus, _complex as C
from mathipy import numeric_operations as ops

class Complex_Function(calculus.Function):
    def __init__(self, f):
        self.f = f

    def calculate_values(self, z):
        if ops.is_scalar(z):
            return self.f(z)
        else:
            return list(map(self.calculate_values, z))

    def __call__(self, z):
        return self.calculate_values(z)

    def plot(self, plot_type='conformal_map', pos=(0,0), rnge=(5,5), **kwargs):
        x_min, x_max = pos[0] - rnge[0], pos[0] + rnge[0]
        y_min, y_max = pos[1] - rnge[1], pos[1] + rnge[1]
        s = kwargs.get('step', 100)
        x = np.linspace(x_min, x_max, s)
        y = np.linspace(y_min, y_max, s)
        X, Y = np.meshgrid(x,y)
        W = np.array(self.calculate_values(X + Y * C.Complex(0,1)))

        if plot_type == 'conformal_map':
            self.conformal_map(X, Y, W, **kwargs)
        
        elif plot_type == 'colour_map':
            self.colour_map(X, Y, W, **kwargs)

        elif plot_type == 'gradient_map':
            self.gradient_map()

        elif plot_type == 'localized_transformation':
            self.localized_transformation_graph()

        else:
            raise NotImplemented(f'{plot_type} graph type is not supported')

        '''
        pos = kwargs.get('position', (0,0))
        z = _complex.Complex.circle_roots(step)
        if pos[0] != 0 or pos[1] != 0:
            z = list(map(lambda z: z + _complex.Complex(*pos)))
        w = self.calculate_values(z)

        z = list(map(_complex.Complex.split, z))
        x, y = list(zip(*z))
        #Separate real parts from imaginary parts 
        #in the output
        w = list(map(_complex.Complex.split, w))
        u, v = list(zip(*w))

        """
        Plot_types: 
        *Conformal map
        *Vector field
        *Color map
        """

        fig, (ax_i, ax_o) = plt.subplots(1, 2)
        fig.suptitle('Graph of $f(z)$')
        #x-axis: real part of the input 
        #y-axis: imaginary part of the input
        ax_i.plot(x, y)
        ax_i.set_xlabel('$x$')
        ax_i.set_ylabel('$y$')
        ax_i.grid()
        ax_i.set_xlim(pos[0] - 3, pos[0] + 3)
        ax_i.set_ylim(pos[1] - 3, pos[1] + 3)

        #x-axis: real part of the output 
        #y-axis: imaginary part of the output
        ax_o.plot(u, v)
        ax_o.set_xlabel('$u$')
        ax_o.set_ylabel('$v$')
        ax_o.grid()
        ax_o.set_xlim(pos[0] - 3, pos[0] + 3)
        ax_o.set_ylim(pos[1] - 3, pos[1] + 3)

        plt.show()'''

    @staticmethod
    def conformal_map(X, Y, W, **kwargs):
        lv = kwargs.get('levels', 50)
        ls= kwargs.get('linestyles', 'solid')
        a = kwargs.get('alpha', 0.65)
        rcc = kwargs.get('rcc', 'b')
        icc = kwargs.get('icc', 'r')
        fig, ax = plt.subplots()
        ax.contour(X, Y, C.real(W), colors=rcc, linestyles=ls, levels=lv, alpha=a)
        ax.contour(X, Y, C.imag(W), colors=icc, linestyles=ls, levels=lv, alpha=a)
        ax.set_xlabel("$x$",fontsize=15)
        ax.set_ylabel("$y$",fontsize=15)
        ax.set_title("Conformal map: lines of constant $u: {\\rm Re}[w]$ and $v: {\\rm Im}[w]$")
        ax.grid()
        plt.show()

    @staticmethod
    def colour_map(X, Y, W, **kwargs):
        cm = kwargs.get('cmap', 'viridis')
        proj = kwargs.get('projection', 'rectilinear')
        w_feature = kwargs.get('output_feature', 'module')

        if w_feature in ('real', 'a'):
            f = C.real
        elif w_feature in ('imag', 'b'):
            f = C.imag
        elif w_feature in ('module', 'mod', 'r'):
            f = C.module
        elif w_feature in ('argument', 'arg', 'theta'):
            f = C.argument

        fig = plt.figure()
        ax = fig.add_subplot(projection=proj)
        ax.set_xlabel('$x$')
        ax.set_ylabel('$y$')
        ax.set_title(f'Colour map of {w_feature} over x and y')
        
        if proj == 'rectilinear':
            cf = ax.contourf(X, Y, f(W), 51, cmap= cm)
        
        elif proj == '3d':
            w = f(W)
            cf = ax.plot_surface(X, Y, f(W), cmap=cm)
            ax.set_zlabel(f'${w_feature}$')

        cbar = fig.colorbar(cf)
        cbar.update_ticks()
        ax.grid()
        plt.show()

