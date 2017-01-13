import argparse
from argparse import RawTextHelpFormatter
import os
import cmd_utils
import file_utils


def gather_files(assign_num):
    result = file_utils.gather_assignment(assign_num)
    file_string = ""
    for (student, present_list, missing_list)  in result:
        if missing_list is not []:
            file_string = "%s%s\n" %(file_string, student)
            for f in missing_list:
                file_string = "%s\t%s\n" %(file_string, f)
            file_string = file_string + "\n\n"

    with open(os.path.join("asgt0%i-ready" %(assign_num), "missing.txt"), "w+") as missing_file:
        missing_file.write(file_string)

    print(file_string)

    return result

def gather_files(assign_num, student_name):
    result = file_utils.refresh_file(assign_num, student_name)

def check_files(assign_num):
    result = file_utils.check_assignment(assign_num)

    missing_files = file_utils.get_files_missing(result)
    present_files = file_utils.get_files_present(result)

    print("Present Files:\n")    
    for i in present_files:
        print("\t"+i)

    print("Missing Files:\n")
    for i in missing_files:
        print("\t"+i)   

def check_files(assign_num, student_name):
    result = file_utils.check_files(file_utils.get_files(assign_num), os.path.join("asgt0%i-ready" %(assign_num), student_name))


def grade_assignment(assign_num):

    #First we gather the files:
    file_list = gather_files(assign_num)

    #Generate list of missing files:


    #write to asgt0N-ready/missing.txt

def grade_student(assign_num, student_name):








def main():
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)

    parser.add_argument('--grade', action='store', dest='grade', default=-1, type=int, help =
    """
    Grade the assignment.  Provide assignment number (1,2,etc...) 
    Gathers files automatically.
    """)

    parser.add_argument('--gather', action='store', dest='grade', default=-1, type=int, help =
    """
    Gather assignment files (or one student's), but do not grade.
    """)

    parser.add_argument('--check', action='store', dest='check', default=-1, type=int, help =
    """
    Check integrity of files, or refresh student files.  
    """)

    parser.add_argument('--print', action='store', dest='print', default=-1, type=int, help =
    """
    Print assignment, or student's files.  
    """)

    parser.add_argument('--student', action='store', dest='student', default=None, type=str, help=
    """
    [optional] which student to select
    """)


    res = parser.parse_args()
    print(res)