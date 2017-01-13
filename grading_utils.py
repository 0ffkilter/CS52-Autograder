"""
Some helper functions for running sml commands

Matthew Gee
Everett "Rett" Bull
January, 2017
"""


def split_string(string, flag):
    """ Splits a string based on the flags

    string:     string to split
    flag:       key to split it based on

    Adapted from code written by Everett Bull
    """

    regex = re.compile('[$][+-][\w.\-\*]*')   # \w is an abbreviation for A-Za-z0-9_

    selectedFlags = set(flag)
    selectedFlags.add('')

    currentFlags = set()

    echo = False

    result = ""
    for line in string :
       newFlags = regex.findall(line)
       if 0 < len(newFlags) :
          for flag in newFlags :
             flagName = flag[2:]
             if flag[1] == '+' and (flagName in selectedFlags) :
                currentFlags.add(flagName)
             elif flag[1] == '-' :
                if flagName == '*' :
                   currentFlags.clear()
                else :
                   currentFlags.discard(flagName)
          echo = 0 < len(currentFlags)
       elif echo :
          result = result + line
    return result


def split_file(read_file, flag):
    with open(read_file, r) as f:
        contents = f.read()
        return split_string (contents, flag)


def format_check(f_name) :
    """
    Return number of lines that are incorrectly formatted

    file:               list of lines in file

    Return Value: (#lines too long, #lines contain tab, #lines)

    Written by Everett Bull
    """

    too_long = 0
    contains_tab = 0
    comments = 0
    linecount = 0

    file = open(f_name, 'r')

    for line in file :
        linecount = linecount + 1
        comments += min(line.count("(*")+ line.count("*)"), 1)
        if 80 < len (line):
           too_long += len(line) - 80
        if 0 <= line.find ("\t") :
           contains_tab += 1

    return (too_long, contains_tab, comments, linecount)
