import argparse
import os
import cmd_utils
import file_utils
import configparser
import grading_utils
import multiprocessing
from argparse import RawTextHelpFormatter
from grading_scripts.student_list import STUDENT_LIST

def print_student(assign_num, student, files=None):
    """Prints a student's files - grabs from from config if no files are
        specified

    assign_num:         assignment number
    student:            which student to print
    files:              what to print (takes from config if none are given)

                        You don't need to specify the name with the file -
                        if you want to print asgt01.sml it will print
                        $student$-asgt01.sml
    """

    if files==None:
        files = file_utils.get_files(assign_num)
    for f in files:
        file_name = os.path.join("asgt0%i-ready" %(assign_num),
                                    student,
                                    "%s-%s" %(student, f))
        cmd_utils.print_file(file_name, assign_num)


def print_assignment(assign_num, student_list=STUDENT_LIST):
    """Prints out an assignemnt files, with the file list taken from the config

    assign_num:         assignment_number
    student_list:       list of students to print (defaults to all)
    """

    files = file_utils.get_files(assign_num)

    for (name, email, section) in student_list:
        print_student(assign_num, student, files)

def check_files(assign_num, verbose=True):
    """Checks which file are present or missing

    assign_num:         which assignment to check

    """
    result = file_utils.check_assignment(assign_num)

    missing_files = file_utils.get_files_missing(result)
    present_files = file_utils.get_files_present(result)

    if verbose is True:
        print("Present Files:\n")
        for i in present_files:
            print("\t" + i)

        print("Missing Files:\n")
        for i in missing_files:
            print("\t" + i)

    return (present_files, missing_files)

def check_files_student(assign_num, student_name):
    """Checks the files for one student

    assign_num:         assignment number
    student_name:       student to check
    """
    result = file_utils.check_files(file_utils.get_files(
        assign_num), os.path.join("asgt0%i-ready" % (assign_num), student_name))


def gather_files(assign_num, overwrite=False, students=STUDENT_LIST):
    """Gathers the files for the appropriate assignment and copies them to
    $assign_num$-ready and generates the sml grading subfiles for each student

    assign_num:         assignment number
    overwrite:          do you overwrite the files already in there?
    students:           which students to use (default all)
    """
     # Load the config file
    config = configparser.ConfigParser()

    config.read(os.path.join("CS52-GradingScripts", "asgt0%i" %(assign_num), "config.ini"))
    num_points = config["Assignment"]["TotalPoints"]
    style_points = config["Assignment"]["StylePoints"]
    num_problems = int(config["Assignment"]["NumProblems"])
    submit_files = config["Assignment"]["Files"].split(",")

    #Gather the files
    file_list = file_utils.move_files(submit_files, "asgt0%i-submissions" %(assign_num), "asgt0%i-ready" %(assign_num))

    #Get the list of problems from the config file and get the appropriate information
    problem_config = []
    for i in range(num_problems):
        cur_num = i + 1
        if "Problems" in config[str(cur_num)]:
            for sub_problem in config[str(cur_num)]["Problems"].split(","):
                problem_config.append(("%i%s" %(cur_num, sub_problem), config["%i%s" %(cur_num, sub_problem)]))
        else:
            problem_config.append((str(cur_num), config[str(cur_num)]))



    # Generate sml subfiles

    # Generate list of strings for each problem

    grading_file_list = []
    problem_strings = []
    #[(pre_string, post_string)]
    for name, problem in problem_config:
        req_list = grading_utils.get_requirements(problem["requirements"], assign_num)

        # Fancy formatting
        pre_string = "\n\n(*=====================Grader Code=====================*)\n"

        # Read from each of the req files

        for r in req_list:
            if r.star
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
        grading_file_list.append(name)

    # now for each student

    print("Generating Subfiles")
    cur_progress = 1
    total_progress = len(students)
    for (student, email, section) in students:
        cmd_utils.progress(cur_student, total_students, student)
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

                g_file.write(content_string + pre_string)

                g_file.write("\nval _ = print(\"(*BEGIN*)\\n\");\n")

                g_file.write(post_string)


    return grading_file_list

def gather_files_student(assign_num, overwrite=False, student_name=""):
    """Gather the files of a particular student

    assign_num:         assignment number
    overwrite:          do you overwrite the exsiting files
    student_name        name to match for gathering
    """
    to_grade = []
    for (name, email, section) in student_list.STUDENT_LIST:
        if student_name in name or student_name in email:
            to_grade.append((name, email, section))
    return gather_files(assign_num, overwrite, to_grade)

def grade_student(assign_num, student, student_file, config, problems, grading_file_list, cur_progress, total_points):

    (name, email, section) = student


    output_string = ""
    summary_list = []
    num_not_compiled = 0

    for p, f in zip(problems, grading_file_list):
        cur_progress = cur_progress + 1
        cmd_utils.progress(cur_progress, total_points, "%s : %s" %(name, p))
        cur_path = os.path.join("asgt0%i-ready" %(assign_num), name, "grading", f)
        output = cmd_utils.run_file(cur_path)

        problem_string = "Problem %s:\n" %(p)
        idx = output.find("(*BEGIN*)")

        num_passed = 0
        num_failed = 0
        if idx == -1:
            problem_string = problem_string + "Failed to Compile %s\n"
            num_not_compiled = num_not_compiled + 1
        else:
            parsed_output = output[idx + 9:]
            problem_string = problem_string + parsed_output + "\n"
            num_passed = parsed_output.count("PASS")
            num_failed = parsed_output.count("FAIL")
        num_halted = int(config[p]["Tests"]) - num_passed - num_failed


        num_points = float(config[p]["Points"])

        points_given = 0

        deduction = (num_halted + num_failed) * 0.5
        if num_passed == 0:
            deduction = num_points
        else:
            deduction = min(num_points-0.5, deduction)

        summary_list.append((p, deduction))
        output_string = output_string + problem_string


    output_string = output_string + "\n\n=====Summary:=====\n\n"

    output_string = output_string + ("Deductions:\nProblem | Points Taken\n" +
                    "\n".join([p.ljust(7) + "|" + str(d).rjust(10) for (p,d) in summary_list]))

    (too_long, contains_tab, comments, linecount) = grading_utils.format_check(student_file)

    output_string = output_string + "\nStyle:\n"

    total_style_points = int(config["Assignment"]["StylePoints"])
    style_points = total_style_points
    if num_not_compiled > 0:
        style_points = style_points - 0.5

    if too_long > 20:
        style_points = style_points - 0.5

    if contains_tab > 0:
        style_points = style_points - 0.5


    output_string = output_string + "Characters:  %i\n" %(too_long)
    output_string = output_string + "Num Tabs  :  %i\n" %(contains_tab)
    output_string = output_string + "Comments  :  %i\n" %(comments)

    output_string = output_string + "\nTotals:\n"


    total_points = int(config["Assignment"]["TotalPoints"])

    total_deduction = sum([b for (a,b) in summary_list])

    output_string = output_string + "Style Points:       %i/%i\n" %(style_points, total_style_points)
    output_string = output_string + "Correctness Points: %i/%i\n" %(total_points - total_deduction, total_points)


    output_string = output_string + "\n=====Grader Comments======\n\n\n\n\n\n\n\n\n\n"
    output_string = output_string + "Total Points:       %i/%i\n" %(style_points + total_points - total_deduction, total_points + total_style_points)
    grade_path = os.path.join("asgt0%i-ready" %(assign_num), name, "grades.txt")
    with open(grade_path, "w+") as f:
        f.write(output_string)

    return cur_progress


def grade_assignment(assign_num, overwrite, students=STUDENT_LIST):
    problems = gather_files(assign_num, overwrite, students)
    grading_file_list = ["asgt0%i_%s.sml" %(assign_num, n) for n in problems]

    config = configparser.ConfigParser()

    config.read(os.path.join("CS52-GradingScripts", "asgt0%i" %(assign_num), "config.ini"))
    num_points = config["Assignment"]["TotalPoints"]
    style_points = config["Assignment"]["StylePoints"]
    num_problems = int(config["Assignment"]["NumProblems"])
    submit_files = config["Assignment"]["Files"].split(",")

    print("Grading asgt0%i" %(assign_num))
    cur_num = 0
    total_files = len(students) * len(problems) + len(students)
    for (name, email, section) in students:
        cur_num = cur_num + 1
        cmd_utils.progress(cur_num, total_files, name)

        """
        p = multiprocessing.Process(target=grade_student, args=((name, email, section),
                                                             assign_num,
                                                             os.path.join("asgt0%i-ready" %assign_num,
                                                                        name,
                                                                        "%s-%s" %(name, submit_files[0])),
                                                             config,
                                                             problems,
                                                             grading_file_list))
        p.start()
        """
        cur_num = grade_student(assign_num,
                        (name, email, section),
                        os.path.join("asgt0%i-ready" %assign_num, name, "%s-%s" %(name, submit_files[0])),
                        config,
                        problems,
                        grading_file_list,
                        cur_num, total_files)

    print("\n")

def grade_assignment_student(assign_num, overwrite=False, student_name=""):
    """grade assignments of students matching student_name

    assign_num:         assignment number
    overwite:           do you overwrite the existing files
    student_name:       student name to match
    """

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



if __name__ == '__main__':
    main()
