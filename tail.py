import time
from optparse import OptionParser

SLEEP_INTERVAL = 0.1


def tail(input_file):
    "Iterate through lines and then tail for further lines."
    while True:
        line = input_file.readline()
        if line:
            yield line
        else:
            _tail_f(input_file)


def _tail_f(input_file):
    "Listen for new lines added to file."
    while True:
        where = input_file.tell()
        line = input_file.readline()
        if not line:
            time.sleep(SLEEP_INTERVAL)
            input_file.seek(where)
        else:
            yield line

def tail_f(input_file):
    input_file.seek(0, 2)
    return _tail_f(input_file)
