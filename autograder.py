import argparse
from argparse import RawTextHelpFormatter
import os
import cmd_utils
import file_utils
import configparser
from grading_scripts.student_list import STUDENT_LIST
import grading_utils


def print_student(assign_num, student, files=None):
    if files=None:
        config = configparser.ConfigParser()
        config.read(os.path.join("CS52-GradingScripts", "asgt0%i" %(assign_num), "config.ini"))
        files = config["Assignment"]["Files"].split(",")

    for f in files:
        file_name = os.path.join("asgt0%i-ready" %(assign_num), student, "%s-%s" %(student, f))
        cmd_utils.print_file(file_name, assign_num)


def print_assignment(assign_num, student_list=STUDENT_LIST):
    config = configparser.ConfigParser()
    config.read(os.path.join("CS52-GradingScripts", "asgt0%i" %(assign_num), "config.ini"))
    files = config["Assignment"]["Files"].split(",")
    
    for (name, email, section) in student_list:
        print_student(assign_num, student, files)


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


def gather_files_student(assign_num, overwrite, student_name):
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


def check_files_student(assign_num, student_name):
    result = file_utils.check_files(file_utils.get_files(
        assign_num), os.path.join("asgt0%i-ready" % (assign_num), student_name))


def grade_assignment(assign_num, overwrite, students=STUDENT_LIST):

    # First we gather the files, but don't overwrite them:
    

    # Load the config file
    config = configparser.ConfigParser()

    config.read(os.path.join("CS52-GradingScripts", "asgt0%i" %(assign_num), "config.ini"))
    num_points = config["Assignment"]["TotalPoints"]
    style_points = config["Assignment"]["StylePoints"]
    num_problems = int(config["Assignment"]["NumProblems"])
    submit_files = config["Assignment"]["Files"].split(",")

   
    file_list = file_utils.move_files(submit_files, "asgt0%i-submissions" %(assign_num), "asgt0%i-ready" %(assign_num))

    problem_config = []
    for i in range(num_problems):
        cur_num = i + 1
        problem_config.append((str(cur_num), config[str(cur_num)]))
        if "Subproblems" in config[str(cur_num)]:
            for sub_problem in config[str(cur_num)]["Subproblems"].split(","):
                problem_config.append(("%i%s" %(cur_num, sub_problem), config["%i%s" %(cur_num, sub_problem)]))

    # Generate sml subfiles

    # Generate list of strings for each problem

    problem_strings = []
    #[(pre_string, post_string)]
    for name, problem in problem_config:
        req_list = grading_utils.get_requirements(problem["requirements"], assign_num)

        # Fancy formatting
        pre_string = "\n\n(*=====================Grader Code=====================*)\n\n"

        # Read from each of the req files
     
        for r in req_list:
            with open(r, "r") as f:
                pre_string = pre_string + f.read() + "\n"

        # Read from the script file
        post_string = ""

        file_name = ""
        if "Script" in problem:
            file_name = problem["Script"]
        else:
            file_name = "asgt0%i_%s.sml" %(assign_num, name)

        with open(os.path.join("CS52-GradingScripts", "asgt0%i" % (assign_num), file_name), "r") as f_grade:
            post_string = f_grade.read()

        # Put into a list
        problem_strings.append((name, pre_string, post_string))

    # now for each student

    for (student, email, section) in students:

        # problems are 1 indexed
        
        # For each of the problem strings
        for (name, pre_string, post_string) in problem_strings:
            # Generate a flag to partition the file
            flag = ""
            if len(name) > 1:
                if name[-1].isalpha():
                    if int(name[:-1]) < 10:    
                        flag = flag + "0%i_0%s" % (assign_num, name)
                    else:
                        flag = flag + "0%i_%s" % (assign_num, name)
                else:
                    flag = flag + "0%i_%s" % (assign_num, name)
            else:
                if int(name) < 10:
                    flag = flag + "0%i_0%s" % (assign_num, name)
                else:
                    flag = flag + "0%i_%s" % (assign_num, name)

            # Partition the student's file
            content_string = grading_utils.split_file(os.path.join(
                "asgt0%i-ready" % (assign_num), student, "%s-%s" %(student, submit_files[0])), flag)

            # Write to a grading file
            if not os.path.exists(os.path.join("asgt0%i-ready" % (assign_num), student, "grading")):
                os.makedirs(os.path.join("asgt0%i-ready" % (assign_num), student, "grading"))
            with open(os.path.join("asgt0%i-ready" % (assign_num), student, "grading", "asgt0%i_%s.sml" % (assign_num, name)), "w+") as g_file:

                g_file.write(content_string + pre_string + post_string)
            
        


def grade_assignment_student(assign_num, overwrite, student_name):

    to_grade = []
    for (name, email, section) in student_list.STUDENT_LIST:
        if student_name in name or student_name in email:
        to_grade.append((name, email, section))
    grade_assignment(assign_num, overwrite, to_grade)


def main():
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)

    parser.add_argument('--grade', action='store', dest='grade', default=-1, type=int, help="""
    Grade the assignment.  Provide assignment number (1,2,etc...) 
    Gathers files automatically.
    """)

    parser.add_argument('--gather', action='store', dest='gather', default=-1, type=int, help="""
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
    
    if res.gather is not -1:
        if res.student is not None:
            gather_files_student(res.gather, res.overwrite, res.student)
        else:
            gather_files(res.gather, res.overwrite)


    if res.check is not -1:
        if res.student is not None:
            check_files(res.check, res.student)
        else:
            check_files(res.check)


    if res.grade is not -1:
        if res.student is not None:
            grade_assignment_student(res.grade, res.overwrite, res.student)
        else:
            grade_assignment(res.grade, res.overwrite)

    if res.print is not -1:
        if res.student is not None:
            print_files_student(res.gather, res.student)
        else:
            print_files(res.gather)



main()