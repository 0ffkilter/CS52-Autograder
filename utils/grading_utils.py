"""
Some helper functions for running sml commands

Matthew Gee
Everett "Rett" Bull
January, 2017
"""
import os
import re
from typing import Text, Dict, List, Tuple

def get_flag(assign_num: int, p: Text, config: Dict):
    if "Flag" in config:
        return "0%i_%s" %(assign_num, config["Flag"])
    flag = ""
    if len(p) > 1:
        if p[-1].isalpha():
            if int(p[:-1]) < 10:
                flag = "0%i_0%s" % (assign_num, p)
            else:
                flag = "0%i_%s" % (assign_num, p)
        else:
            flag = "0%i_%s" % (assign_num, p)
    else:
        if int(p) < 10:
            flag = "0%i_0%s" % (assign_num, p)
        else:
            flag = "0%i_%s" % (assign_num, p)

    return flag

def parse_problems(config: Dict) -> List[Tuple[Text, Text, Dict]]:
    """
    Returns a list of triples of problems
    [(problem_name, problem_type, data)]


    """
    return_list = []
    num_problems = config["Assignment"]["NumProblems"]

    assign_mode="sml"
    if "Mode" in config["Assignment"]:
        assign_mode = config["Assignment"]["Mode"]


    #Mode Priorities:
    #Problem > Parent Problem > Assignment
    for i in range(num_problems):
        cur_mode = assign_mode
        cur_num = i + 1
        cur_str = str(cur_num)
        if "Mode" in config[cur_str]:
            cur_mode = config[cur_str]["Mode"]
        if "Problems" in config[cur_str]:
            for sub_problem in config[cur_str]["Problems"].split(","):
                cur_prob = "%i%s" %(cur_num, sub_problem)
                if "Mode" in config[cur_prob]:
                    cur_mode = config[cur_prob]["Mode"]
                return_list.append((
                            "%i%s" %(cur_num, sub_problem),
                            cur_mode,
                            config["%i%s" %(cur_num, sub_problem)]))
        else:
            return_list.append((
                        cur_str,
                        cur_mode,
                        config[cur_str]
                        ))
    return return_list


#Deprecated
def get_requirements(requirements, assign_num):
    """Gets the requirements string from the path"

    requirements:
    """

    req_list = requirements.split(",")
    return_list = []
    for req in req_list:
        cur_path = None
        if "$FILE$" in req:
            cur_req = req.split("/")[-1]
            cur_path = os.path.join("CS52-GradingScripts",
                                    "asgt0%i" % (assign_num), cur_req + ".sml")
            if os.path.exists(cur_path):
                return_list.append(cur_path)
        else:
            """
            req_parts = req.split("_")
            if req_parts[-1] == "exact":
                return_list.append("list_compare_exact")
            elif req_parts[-1] == "list":
                return_list.append("list_compare")
            elif req_parts[-1] == "knuth":
                return_list.append("list_compare")
                return_list.append("list_compare_exact")
            """
            return_list.append(req)
    return return_list


def split_string(string: Text, flag: Text, select_all: bool = True) -> Text:
    """ Splits a string based on the flags

    string:     string to split
    flag:       key to split it based on

    Adapted from code written by Everett Bull
    """

    # \w is an abbreviation for A-Za-z0-9_

    string = string.replace("\t", "    ")
    regex = re.compile('[$][+-][\w.\-\*]*')

    selectedFlags = set([flag])
    if select_all:
        selectedFlags.add('')

    currentFlags = set()

    echo = False

    result = ""
    for line in string.split("\n"):
        newFlags = regex.findall(line)
        if 0 < len(newFlags):
            for flag in newFlags:
                flagName = flag[2:]
                if flag[1] == '+' and (flagName in selectedFlags):
                    currentFlags.add(flagName)
                elif flag[1] == '-':
                    if flagName == '*':
                        currentFlags.clear()
                    else:
                        currentFlags.discard(flagName)
            echo = 0 < len(currentFlags)
        elif echo:
            result = f"{result}\n{line}"
    return result

def parse_a52(name: Text, output: Text, expected_answer: Text) -> (Text, bool):
    """
    
    """
    pat = re.compile("CS52 says > (\d*)")

    res = pat.search(output)

    fail_ans = ""
    if res is not None:
        if res.groups(0)[0] == expected_answer:
            return ("%s:\tPASS" %(name), True)
        else:
            fail_ans = res.groups(0)[0]

    if "error" in output:
        return ("%s:\tFAIL\n\tExpected: %s\n\tActual: %s\n\tError Encountered, output as follows:\n%s" %(name, expected_answer, fail_ans, output), False)
    return ("%s:\tFAIL\n\tExpected: %s\n\tActual: %s" %(name, expected_answer, fail_ans), False)


def split_file(read_file: Text, flag: Text) -> Text:
    with open(read_file, 'r') as f:
        contents = f.read()

        return split_string(contents, flag)

#print(split_file(os.path.join("asgt01-ready", "Abele", "Abele-asgt01.sml"), "01_01"))

def format_check(f_name: str) -> (int, int, int, int):
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
    if os.path.exists(f_name):
        file = open(f_name, 'r')

        for line in file:
            linecount = linecount + 1
            comments += min(line.count("(*") + line.count("*)"), 1)
            if 80 < len(line):
                too_long += len(line) - 80
            if 0 <= line.find("\t"):
                contains_tab += 1

    return (too_long, contains_tab, comments, linecount)

