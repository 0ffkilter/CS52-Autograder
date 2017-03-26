import argparse
import os
import sys
import configparser
from utils import file_utils, cmd_utils, grading_utils
import multiprocessing
import datetime
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
        print("Present Files:")
        for i in present_files:
            print("\t" + i)

        print("Missing Files:")
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
    $assign_num$-ready

    assign_num:         assignment number
    overwrite:          do you overwrite the files already in there?
    students:           which students to use (default all)
    """
     # Load the config file


    config = configparser.ConfigParser()


    config.read(os.path.join("CS52-GradingScripts", "asgt0%i" %(assign_num), "config.ini"))

    submit_files = config["Assignment"]["Files"].split(",")
    submit_files = [f.strip() for f in submit_files]


    file_list = file_utils.move_files(submit_files, "asgt0%i-submissions" %(assign_num), "asgt0%i-ready" %(assign_num), stdt_list=students)

    with open(os.path.join("asgt0%i-ready" %(assign_num), "files.txt"), 'w+') as f:
        for (name, present_list, missing_list) in file_list:
            f.write(name + "\n")
            if len(present_list) > 0:
                f.write("\tPresent:\n")
                for p in present_list:
                    f.write("\t\t%s\n" %(p))

            if len(missing_list) > 0:
                f.write("\tMissing:\n")
                for m in missing_list:
                    f.write("\t\t%s\n" %(m))
            f.write("\n")


def generate_a52(assign_num, students=STUDENT_LIST):
    config = configparser.ConfigParser()

    problem_config = []
    for i in range(num_problems):
        cur_num = i + 1
        if "Problems" in config[str(cur_num)]:
            for sub_problem in config[str(cur_num)]["Problems"].split(","):
                problem_config.append(("%i%s" %(cur_num, sub_problem), config["%i%s" %(cur_num, sub_problem)]))
        else:
            problem_config.append((str(cur_num), config[str(cur_num)]))

    mul_path = os.path.join("CS52-GradingScripts", "asgt0%i" %(assign_num), "resources", "mullib.a52")


    for (student, email, section) in students:
        shutil.copy(mul_path, os.path.join("asgt0%i-ready" %(assign_num), student, "mullib.a52"))
    return problem_config


def generate_subfiles(assign_num, overwrite=False, students=STUDENT_LIST):


    config = configparser.ConfigParser()


    config.read(os.path.join("CS52-GradingScripts", "asgt0%i" %(assign_num), "config.ini"))
    num_points = config["Assignment"]["TotalPoints"]

    style_points = 2
    if "StylePoints" in config["Assignment"]:
        style_points = config["Assignment"]["StylePoints"]

    num_problems = int(config["Assignment"]["NumProblems"])
    submit_files = config["Assignment"]["Files"].split(",")


    files_to_copy = []
    if "Resources" in config["Assignment"]:
        files_to_copy = config["Assignment"]["Resources"].split(",")
        files_to_copy = [f.strip() for f in files_to_copy]
    #Gather the files



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

    pregrade_string = ""
    with open(os.path.join("pregrade_files", "pregrade.sml"), 'r') as pregrade:
        pregrade_string = pregrade.read()

    # (name (number), flag, pregrade_code (not problems), test_script)

    problem_list = []
    for (name, config_problem) in problem_config:
        problem_number = name
        problem_name = config_problem["Name"]
        problem_requirements = grading_utils.get_requirements(config_problem["requirements"], assign_num)
        problem_flag = grading_utils.get_flag(assign_num, problem_number)

        pre_string = "\n\n(*=====================Grader Code=====================*)\n"

        for r in problem_requirements:
            if os.path.exists(r):
                with open(r, "r") as f:
                    pre_string = pre_string + f.read() + "\n"
            else:
                pre_string = pre_string + grading_utils.split_string(pregrade_string, r)

        if "Script" in problem_config:
            file_name = problem_config["Script"]
        else:
            file_name = "asgt0%i_%s.sml" %(assign_num, name)

        pre_string = pre_string + "\n\nval _ = print(\"(*BEGIN*)\\n\");\n"

        with open(os.path.join("CS52-GradingScripts", "asgt0%i" % (assign_num), file_name), "r") as f_grade:
            pre_string = pre_string + f_grade.read()
        grading_file_list.append((problem_number, problem_name))
        problem_list.append((
                            problem_number,
                            problem_name,
                            problem_flag,
                            pre_string))
    # now for each student

    pre_content = ""
    if 'PreFile' in config["Assignment"]:
        with open(os.path.join("CS52-GradingScripts", "asgt0%i" %(assign_num), config["Assignment"]["PreFile"]), 'r') as f:
            pre_content = f.read()

    print("\nGenerating Subfiles")
    cur_progress = 1
    total_progress = len(students)
    for (student, email, section) in students:
        cmd_utils.progress(cur_progress, total_progress, student)
        # problems are 1 indexed

        # For each of the problem strings

        student_file = os.path.join(
                "asgt0%i-ready" % (assign_num), student, "%s-%s" %(student, submit_files[0]))
        student_code = ""
        try:
            with open(student_file, 'r') as s_file:
                student_code = s_file.read().replace("\t", "    ")


            #Generate the code associated with each problem
            #Yes, this should be a dictionary but I don't
            #want to have worry about ordering a dictionary
            problem_code = []
            for p in problem_list:
                problem_code.append((p[1], grading_utils.split_string(student_code, p[2]), []))

            #Reverse the list and do it this way
            #Because the normal way is too much work
            #...yeah

            problem_code = problem_code[::-1]

            new_problem_code = []
            for i in range(len(problem_code)):

                p, p_code, p_sub = problem_code[i]
                for j in range(i, len(problem_code)):
                    p2, p2_code, p2_sub = problem_code[j]
                    if p2 in p_code:
                        if p2 in p_sub:
                            pass
                        else:
                            p_sub = p_sub + [p2] + p2_sub
                new_problem_code.append((p, p_code, p_sub))

            new_problem_code = new_problem_code[::-1]

            problem_code = []
            for name, code, sub_problems in new_problem_code:
                for sub in sub_problems:
                    for n, c, s in problem_code:
                        if (n == sub and n != name):
                            code = c + code
                problem_code.append((name, code, sub_problems))

            for ((number, name, flag, grading_string), (name2, code, sub_problems)) in zip(problem_list, problem_code):
                if not os.path.exists(os.path.join("asgt0%i-ready" % (assign_num), student, "grading")):
                    os.makedirs(os.path.join("asgt0%i-ready" % (assign_num), student, "grading"))
                with open(os.path.join("asgt0%i-ready" % (assign_num), student, "grading", "asgt0%i_%s.sml" % (assign_num, name)), "w+") as g_file:

                    g_file.write(pre_content + code + grading_string)



        except  FileNotFoundError:
            pass
            #File not found
        except:
            print("Unexpected error:", sys.exc_info()[0])

        cur_progress = cur_progress + 1
    print()
    return grading_file_list


def generate_subfiles_student(assign_num, student, overwrite=False):
    to_grade = []
    pattern = re.compile(student_name)
    for (name, email, section) in student_list.STUDENT_LIST:
        if pattern.match(name).group(0) != '' or pattern.match(email).group(0):
            to_grade.append((name, email, section))
    return generate_subfiles(assign_num, overwrite, to_grade)

def gather_files_student(assign_num, overwrite=False, student_name=""):
    """Gather the files of a particular student

    assign_num:         assignment number
    overwrite:          do you overwrite the exsiting files
    student_name        name to match for gathering
    """
    to_grade = []
    pattern = re.compile(student_name)
    for (name, email, section) in student_list.STUDENT_LIST:
        if pattern.match(name).group(0) != '' or pattern.match(email).group(0):
            to_grade.append((name, email, section))
    return gather_files(assign_num, overwrite, to_grade)


def grade_student(assign_num, student, student_file, config, problems, cur_progress, total_points):


    #Parse the Information out of the studnet name
    (name, email, section) = student

    #Generate the timestamps of the files submitted
    timestamps = ""
    with open(os.path.join("asgt0%i-ready" %(assign_num), name, ".timestamps.txt"), 'r') as t:
        timestamps = t.read()

    timestamp_list = timestamps.split("\n")
    timestamps = []

    for t in timestamp_list:
        if ',' in t:
            l = t.split(",")
            timestamps.append((l[0],l[1]))


    #Adjust the timezone and format the string
    timestamp_string = ""
    try:
        for (f, t) in timestamps:
            time = datetime.datetime.strptime(t, "%Y-%m-%d %H:%M:%S")
            due_date = datetime.datetime.strptime(config["Assignment"]["DueDate"], "%Y-%m-%d %H:%M:%S")
            if time < due_date:
                timestamp_string = timestamp_string + ("  %s" %(f)).ljust(19) + "%s\n" %(time.strftime("%b %d, %H:%M:%S"))
            else:
                timestamp_string = timestamp_string + ("  %s" %(f)).ljust(19) + "%s (LATE)\n" %(time.strftime("%b %d, %H:%M:%S"))
    except:
        pass

    #Base for the output string
    output_string = """
Name:              %s
Email:             %s
Section:           %s
Submission Date:
%sAssignment Num:    %i\n\n
""" %(name,
    email,
    section,
    timestamp_string,
    assign_num
    )

    summary_list = []
    num_not_compiled = 0

    #Run each of the files in student_name/grading


    #0 = sml
    #1 = a52
    #2 = a52 pipe
    mode = 0

    #Problem mode overrites assignment mode

    if not "Mode" in config["Assignment"] or 
        config["Assignment"]["Mode"] == "sml" or 
        config["Assignment"]["Mode"] == "":
        for p, n in problems:
            f = "asgt0%i_%s.sml" %(assign_num, f)
            #Adjust progress bar
            cur_progress = cur_progress + 1
            cmd_utils.progress(cur_progress, total_points, "%s : %s" %(name, p))

            #Get the path offile we're going to run and run it
            cur_path = os.path.join("asgt0%i-ready" %(assign_num), name, "grading", f)
            output = cmd_utils.run_file(cur_path)

            #Parse the output
            problem_string = "Problem %s:\n" %(p)
            idx = output.find("(*BEGIN*)")

            #Count the results based onw hat we expect
            num_passed = 0
            num_failed = 0
            if idx == -1:
                problem_string = problem_string + "Failed to Compile\n\tCheck %s for errors\n\n" %(cur_path)
                num_not_compiled = num_not_compiled + 1
            else:
                parsed_output = output[idx + 9:]
                if parsed_output[-3] == '-':
                    parsed_output = parsed_output[:-3] + "\n"
                problem_string = problem_string + parsed_output + "\n"
                num_passed = parsed_output.count("PASS")
                num_failed = parsed_output.count("FAIL")

            #Tests that didn't pass
            num_halted = int(config[p]["Tests"]) - num_passed - num_failed

            #Get the number of points in this problem
            num_points = float(config[p]["Points"])

            #Deduct points
            deduction = (num_halted + num_failed) * 0.5
            if num_passed == 0:
                deduction = num_points
            else:
                deduction = min(num_points-0.5, deduction)

            #Append to thel ist of deductions
            summary_list.append((p, deduction))
            output_string = output_string + problem_string
    elif config["Assignment"]["Mode"] == "a52":
        for p, c_p in problems:
            cur_progress = cur_progress + 1
            cmd_utils.progress(cur_progress, total_points, "%s : %s" %(name, p))

            to_run = ""
            if "File" in c_p:
                to_run = c_p["File"]
            else:
                to_run = c_p["Name"][:c_p["Name"].find("_")]
            cur_path = os.path.join("asgt0%i-ready" %(assign_num), name, "%s.a52" %(to_run))
            answer_file = os.path.join("CS52-GradingScripts", "asgt0%i" %(assign_num), "%s.a52" %(c_p["Name"]))

            output = cmd_utils.run_a52(cur_path, answer_file, assign_num=assign_num)

            result, did_pass = grading_utils.parse_a52(c_p["Name"], output, c_p["Answer"])

            deduction = 0
            if not did_pass:
                deduction = float(c_p["Points"])
            summary_list.append(p, c_p["Name"], deduction)

            output_string = "\n" + output_string + "\n"



    #Format the summary and rest of it
    output_string = output_string + "\n\n=====Summary:=====\n\n"


    #Print the deductions
    if config["Assignment"]["Mode"] == "a52":
        output_string = output_string + ("Deductions:\nProblem | Points Given\n" +
                    "\n".join([n.ljust(8) + "|" + (str(float(config[p]["Points"]) - d) + "/" + config[p]["Points"]).rjust(10) for (p,n,d) in summary_list]))

    else:
        output_string = output_string + ("Deductions:\nProblem | Points Given\n" +
                    "\n".join([p.ljust(8) + "|" + (str(float(config[p]["Points"]) - d) + "/" + config[p]["Points"]).rjust(10) for (p,d) in summary_list]))

    #Format check the assignment
    (too_long, contains_tab, comments, linecount) = grading_utils.format_check(student_file)

    output_string = output_string + "\nStyle:\n"

    total_style_points = int(config["Assignment"]["StylePoints"])
    style_points = total_style_points
    if num_not_compiled > 0:
        style_points = style_points - 0.5

    if too_long > 20:
        style_points = style_points - 0.5

    style_points = max(0, style_points)

    #I don't care about tabs
    #if contains_tab > 0:
        #style_points = style_points - 0.5

    #Style summary
    output_string = output_string + "Characters:  %i\n" %(too_long)
    output_string = output_string + "Num Tabs  :  %i\n" %(contains_tab)
    output_string = output_string + "Comments  :  %i\n" %(comments)

    output_string = output_string + "\nTotals:\n"

    #Rest of it
    total_points = int(config["Assignment"]["TotalPoints"])

    total_deduction = sum([b for (a,b) in summary_list])

    output_string = output_string + "Style Points:       %.1f/%i\n" %(style_points, total_style_points)
    output_string = output_string + "Correctness Points: %.1f/%i\n" %(total_points - total_deduction, total_points)


    output_string = output_string + "\n=====Grader Comments======\n\n\n\n\n\n\n\n\n\n"
    output_string = output_string + "Total Points:       %.1f/%i\n" %(style_points + total_points - total_deduction, total_points + total_style_points)
    grade_path = os.path.join("asgt0%i-ready" %(assign_num), name, "grades.txt")
    with open(grade_path, "w+") as f:
        f.write(output_string)

    return cur_progress


def grade_assignment(assign_num, overwrite, num_partitions=-1, students=STUDENT_LIST):
    gather_files(assign_num, overwrite, students)

    config = configparser.ConfigParser()
    config.read(os.path.join("CS52-GradingScripts", "asgt0%i" %(assign_num), "config.ini"))

    problems = []
    if "Mode" in config["Assignment"]:
        if config["Assignment"]["Mode"] == "sml":
            problems = generate_subfiles(assign_num, overwrite, students)
        if config["Assignment"]["Mode"] == "a52":
            problems = generate_a52(assign_num, students)
    else:
        #Assume it's sml
        problems = generate_subfiles(assign_num, overwrite, students)
    #Parse the config file
    

    num_points = config["Assignment"]["TotalPoints"]
    style_points = config["Assignment"]["StylePoints"]
    num_problems = int(config["Assignment"]["NumProblems"])
    submit_files = config["Assignment"]["Files"].split(",")
    submit_files = [f.replace(" ", "") for f in submit_files]

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
                        cur_num, total_files)


    print("\n")
    if num_partitions is not -1:
        file_utils.partition_assignment(assign_num, num_partitions)

def grade_assignment_student(assign_num, overwrite=False, student_name=""):
    """grade assignments of students matching student_name

    assign_num:         assignment number
    overwite:           do you overwrite the existing files
    student_name:       student name to match
    """

    to_grade = []
    for (name, email, section) in STUDENT_LIST:
        if student_name in name or student_name in email:
            to_grade.append((name, email, section))
    grade_assignment(assign_num, overwrite, students=to_grade)


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

    parser.add_argument('--print', action='store', dest='print_var', default=-1, type=int, help="""
    Print assignment, or student's files.
    """)

    parser.add_argument('--student', action='store', dest='student', default=None, type=str, help="""
    [optional] which student to select
    """)

    parser.add_argument('--generate', action='store', dest='generate', default=-1, type=int, help="""
    Regenerate subfiles for grading
    """)

    parser.add_argument('-overwrite', action='store_true', dest='overwrite', help="""
    [optional] force refresh the files, overwriting any changes made to local files.
    """)

    parser.add_argument('--zip', action='store', dest='num_partitions', default=-1, type=int, help="""
    [optional] zip the assignment for distribution - only works with --grade as well
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

    if res.generate is not -1:
        if res.student is not None:
            generate_subfiles_student(res.generate, res.student)
        else:
            generate_subfiles(res.generate)

    if res.grade is not -1:
        if res.student is not None:
            grade_assignment_student(res.grade, res.overwrite, res.student)
        else:
            grade_assignment(res.grade, res.overwrite, res.num_partitions)

    if res.print_var is not -1:
        if res.student is not None:
            print_files_student(res.gather, res.student)
        else:
            print_files(res.gather)




if __name__ == '__main__':
    main()
