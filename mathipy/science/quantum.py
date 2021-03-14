from mathipy.linalg import Vector, Matrix
import mathipy as mpy
import numpy as np

def ket(n: int, l: int= -1) -> Vector:
    #TODO
    if l == -1:
        pass
    e = [0 if n != i else 1 for i in range(l + 1)]

H = Matrix((1 / mpy.sqrt2) * np.array(
    [
        [1,  1],
        [1, -1]
    ]  
))
#TODO
#Add quantum gates
