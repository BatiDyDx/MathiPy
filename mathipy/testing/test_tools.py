from time import time
from datetime import timedelta

def test_time(f):
    def wrapper(*args, **kwargs):
        start_time = time()
        f(*args, **kwargs)
        end_time = time()
        x = end_time - start_time
        total_time = timedelta(seconds=x)
        if x < 60:
            return 'Total seconds: ' + str(total_time.total_seconds())
        else:
            return 'Total time: ' + str(total_time)
    return wrapper
