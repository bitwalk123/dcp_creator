import logging
import time


def is_num(s: str):
    """
    is_num
    check if string can be converted to number

    :return: bool
    """
    try:
        float(s)
    except ValueError:
        return False
    else:
        return True


def timeit(f: callable):
    """
    decolator for benchmark
    """
    def wrap(*args, **kwargs):
        time_start = time.time()
        ret = f(*args, **kwargs)
        time_end = time.time()
        elapsed = (time_end - time_start)
        print('>>> {:s} function took {:.3f} sec'.format(f.__name__, elapsed))

        return ret

    return wrap


def getAppLogger(name):
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler('logger.log')
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(levelname)-9s  %(asctime)s  [%(name)s] %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def convert_dcp_dict2colname(dict_dcp):
    list_sensor_step = dict_dcp['sensor_steps']
    list_stat = dict_dcp['statistics']
    list_colname = list()
    for dict_sensor_step in list_sensor_step:
        sensor = dict_sensor_step['sensor']
        step = dict_sensor_step['step']
        for stat in list_stat:
            list_colname.append('%s_%s_%s' % (sensor, step, stat))
    return list_colname
