import os
import datetime
import platform
from databasetools import CSV
from psutil import virtual_memory
try:
    import multiprocess as mp
    CPUs = mp.cpu_count()
except ModuleNotFoundError:
    CPUs = 'N/A'


directory = os.path.join(os.path.dirname(__file__), 'data')
# file_name = 'plan_l.pdf'
# file_name = 'plan_p.pdf'
# file_name = 'article.pdf'
# file_name = 'document.pdf'
file_name = 'con docs2.pdf'
# file_name = 'con docs2_sliced.pdf'
pdf = os.path.join(directory, file_name)


def write_log(file_path, log):
    if os.path.isfile(file_path):
        CSV(file_path).append(log)
    else:
        CSV(file_path).write(log)


def dump_log(test_case=None, time=None, result=None):
    MEM = virtual_memory()
    now = datetime.datetime.now()
    date_time = str(now).split('.', 1)[0]
    fname = test_case[0] + '.csv'
    file_path = os.path.join(os.path.dirname(__file__), 'log', fname)

    rows = [date_time, test_case[-2], test_case[-1], file_name, result, str(round(time, 2)), platform.python_version(),
            platform.system(), CPUs, MEM.total >> 30]
    return rows, file_path


__all__ = ['pdf', 'directory', 'dump_log', 'write_log']
