"""
Some helper functions for running sml commands

Matthew Gee
January, 2017
"""

import os
import sys
import signal
from subprocess import PIPE, TimeoutExpired, Popen
from platform import platform
from time import monotonic as timer

def progress(count, total, suffix=''):
    """
    Prints a progress bar

    Taken from stackoverflow

    """
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)

    if percents == 100.0:
        bar = '=' * (filled_len) + '-' * (bar_len - filled_len)

        sys.stdout.write('\x1b[4;32;40m' + '[%s] %s%s ...%s\r\x1b[0m' % (bar, percents, '%', "Done!".ljust(20)))
        sys.stdout.flush()
    else:
        bar = '=' * (filled_len - 1) + '>' + '-' * (bar_len - filled_len)

        sys.stdout.write('\x1b[4;33;40m' + '[%s] %s%s ...%s\r\x1b[0m' % (bar, percents, '%', suffix.ljust(20)))
        sys.stdout.flush()


def print_file(file, asgt):
    """
    Prints a file

    file_name:          name of file to print
    asgt_name:          Title of file

    Return Value: none
    """
    try:

        cmd = r'lpr %s -T %s -P %s -o cpi=14 -o lpi=8 -o sides=two-sided-long-edge -o page-left=72 -o page-right=72 -o prettyprint' %(file, asgt, PRINTER_NAME)
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        result = proc.communicate()[0].decode("utf-8").splitlines()
    except:
        print('lpr error \n')
        return;


def run_string(command, timeout=5, output_file=".tmp.sml", delete=True):
    """Returns output of running a string through the sml interpreter

    Example: run_string("val foo = 5;")

    command:        string to run
    timeout:        timeout of command
    output_file:    where to put the text
    delete:         do we delete the file afterwards
    """
    with open(output_file, 'w+') as f:
        f.write(command)

    return run_file(output_file, timeout, delete)


def run_file(read_file, timeout=5, delete=False):
    """Runs a file through the sml intpreter

    read_file:      file to run
    timeout:        timeout of command
    delete:         do we delete the file afterwards
    """
    if not os.path.exists(read_file):
        return "File Not Found"

    prefix = "cat"
    if platform().find("Windows") != -1:
        prefix = "type"  #Windows Compatability!

    cmd = "%s %s | sml" %(prefix, read_file)

    start = timer()
    with Popen(cmd, shell=True, stdout=PIPE, preexec_fn=os.setsid) as process:
        try:
            output = process.communicate(timeout=timeout)[0]
            output = output.decode('ascii')
        except TimeoutExpired:
            os.killpg(process.pid, signal.SIGINT) # send signal to the process group
            output = process.communicate()[0]

    if delete:
        os.remove(read_file)    

    return output
