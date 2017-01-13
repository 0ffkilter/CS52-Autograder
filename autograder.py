import argparse
from argparse import RawTextHelpFormatter
import os
import cmd_utils
import file_utils
import configparser
from grading_scripts.student_list import STUDENT_LIST
import grading_utils


def gather_files(assign_num, overwrite=False):
    result = file_utils.gather_assignment(assign_num, overwrite)
    file_string = ""
    for (student, present_list, missing_list) in result:
        if missing_list is not []:
            file_string = "%s%s\n" % (file_string, student)
            for f in missing_list:
                file_string = "%s\t%s\n" % (file_string, f)
                file_string = file_string + "\n\n"

    with open(os.path.join("asgt0%i-ready" % (assign_num), "missing.txt"), "w+") as missing_file:
        missing_file.write(file_string)

    return (result, file_string)


def gather_files(assign_num, student_name):
    result = file_utils.refresh_file(assign_num, student_name)


def check_files(assign_num):
    result = file_utils.check_assignment(assign_num)

    missing_files = file_utils.get_files_missing(result)
    present_files = file_utils.get_files_present(result)

    print("Present Files:\n")
    for i in present_files:
        print("\t" + i)

    print("Missing Files:\n")
    for i in missing_files:
        print("\t" + i)


def check_files(assign_num, student_name):
    result = file_utils.check_files(file_utils.get_files(
        assign_num), os.path.join("asgt0%i-ready" % (assign_num), student_name))


def grade_assignment(assign_num, students=STUDENT_LIST):

    # First we gather the files, but don't overwrite them:
    file_list, missing_string = gather_files(assign_num)

    # Load the config file
    config = configparser.ConfigParser()

    config.read("CS52-GradingScripts/asgt0%i/config.ini")

    num_points = config["Assignment"]["TotalPoints"]
    style_points = config["Assignment"]["StylePoints"]
    num_problems = int(config["Assignment"]["NumProblems"])
    submit_file = config["Assignment"]["File"]

    problem_config = []
    for i in range(num_problems):
        cur_num = str(i + 1)
        problem_config.append((config[cur_num]["Requirements"],
                               config[cur_num]["Points"],
                               config[cur_num]["Tests"],
                               config[cur_num]["Script"]))

    # Generate sml subfiles

    # Generate list of strings for each problem

    problem_strings = []
    #[(pre_string, post_string)]
    for i in range(problem_config):
        (reqs, points, tests, file_name) = problem_config[i]

        # Get the requirements list for the scripts
        req_list = grading_utils.get_requirements(reqs, assign_num)

        # Fancy formatting
        pre_string = "=====================Grader Code====================="

        # Read from each of the req files
        for r in reqs:
            with open(r, "r") as f:
                pre_string = pre_string + f.read() + "\n"

        # Read from the script file
        post_string = ""
        with open(os.path.join("CS52-GradingScripts", "asgt0%i" % (assign_num), file_name), "r") as f_grade:
            post_string = f_grade.read()

        # Put into a list
        problem_strings.append((pre_string, post_string))

    # now for each student
    for (student, email, section) in students:
        directory = os.path.join("asgt0%i" % (assign_num), student, "grading")
        if not os.path.exists(directory):
            os.makedirs(directory)

        # problems are 1 indexed
        p = 1
        # For each of the problem strings
        for (pre_string, post_string) in problem_strings:
            # Generate a flag to partition the file
            flag = ""
            if p < 10:
                flag = flag = "0%i_0%i" % (assign_num, p)
            else:
                flag = flag = "0%i_%i" % (assign_num, p)

            # Partition the student's file
            content_string = grader_utils.split_file(os.path.join(
                "asgt0%i-ready" % (assign_num), student, submit_file), flag)

            # Write to a grading file
            with open(os.path.join("asgt0%i-ready" % (assign_num), student, "grading", "asgt0%i_%i" % (assign_num, p)), "w+") as g_file:
                g_file.write(content_string)
                g_file.write(pre_string)
                g_file.write(post_string)
            p = p + 1


def grade_student(assign_num, student_name):
    grade_assignment(assign_num, [student_name])


def main():
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)

    parser.add_argument('--grade', action='store', dest='grade', default=-1, type=int, help="""
    Grade the assignment.  Provide assignment number (1,2,etc...) 
    Gathers files automatically.
    """)

    parser.add_argument('--gather', action='store', dest='grade', default=-1, type=int, help="""
    Gather assignment files (or one student's), but do not grade.
    """)

    parser.add_argument('--check', action='store', dest='check', default=-1, type=int, help="""
    Check integrity of files, or refresh student files.  
    """)

    parser.add_argument('--print', action='store', dest='print', default=-1, type=int, help="""
    Print assignment, or student's files.  
    """)

    parser.add_argument('--student', action='store', dest='student', default=None, type=str, help="""
    [optional] which student to select
    """)

    parser.add_argument('-overwrite', action='store_true', dest='overwrite', help="""
    [optional] force refresh the files, overwriting any changes made to local files.  
    """)

    res = parser.parse_args()
    print(res)
