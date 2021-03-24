from time import time
from datetime import timedelta

def test_time(f):
    def wrapper(*args, **kwargs) -> None:
        start_time = time()
        f(*args, **kwargs)
        end_time = time()
        x = end_time - start_time
        total_time = timedelta(seconds=x)
        if x < 60:
            print('Total seconds: ' + str(total_time.total_seconds()))
        else:
            print('Total time: ' + str(total_time))
    return wrapper

from numpy import vectorize
@vectorize
def is_equal_to(x, y, d: int= 5) -> bool:
    thresh = 5 * 10 ** (-d)
    return abs(x - y) > thresh