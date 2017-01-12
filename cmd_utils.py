"""
Some helper functions for running sml commands

Matthew Gee
January, 2017
"""

import os
from subprocess import PIPE, check_output
from platform import platform



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


def run_file(read_file, timeout=5, delete=True):
    """Runs a file through the sml intpreter
    
    read_file:      file to run
    timeout:        timeout of command
    delete:         do we delete the file afterwards
    """
    prefix = "cat"
    if platform().find("Windows") != -1:
        prefix = "type"  #Windows Compatability!

    cmd = "%s %s | sml" %(prefix, read_file)

    output = check_output(cmd, shell=True, timeout=timeout)

    if delete:
        os.remove(read_file)

    return output
