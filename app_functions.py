import time


def is_num(s: str):
    """
    Reference
    https://note.nkmk.me/python-str-num-determine/

    :return: bool
    """
    try:
        float(s)
    except ValueError:
        return False
    else:
        return True


def timeit(f: callable):
    def wrap(*args, **kwargs):
        time_start = time.time()
        ret = f(*args, **kwargs)
        time_end = time.time()
        elapsed = (time_end - time_start)
        print('{:s} function took {:.3f} sec'.format(f.__name__, elapsed))

        return ret

    return wrap
