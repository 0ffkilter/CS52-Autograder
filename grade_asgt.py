from grading_scripts.data.student_list import STUDENT_LIST
from lib.assignment import Assignment
from lib.student import Student
from os import path, getcwd
from utils.file_utils import move_files
from joblib import Parallel, delayed


def grade_student(s: Student):
    try:
        print(s.name)
        s.generate_subfiles("asgt02.sml")
        s.run_all()
        s.export_results()
    except ConnectionRefusedError:
        pass


if __name__ == '__main__':

    assignment_number = 2

    asgt01 = Assignment(assignment_number)

    assignment_path = path.join(getcwd(), "assignments", "asgt02")

    print([v.mode for k, v in asgt01.problems.items()])
    """
    move_files(["asgt02.sml"],
               path.join(assignment_path, "asgt02-submissions"),
               path.join(assignment_path, "asgt02-ready"),
               False,
               STUDENT_LIST)
    """
    students = []

    default_student_dir = path.join(assignment_path, "asgt02-ready")

    start_letter = 'A'
    has_started = False

    port_count = 3000
    for (name, alias, email, section) in STUDENT_LIST:
        if name is not "ChenBr":
            continue
        students.append(Student(
            name,
            alias,
            email,
            section,
            asgt01,
            path.join(default_student_dir, name),
            port_count
        ))
        port_count = port_count + 100
    print(students)
    grade_student(students[0])
    stdt_list = []
    for s in students:
        if has_started:
            stdt_list.append(s)
            continue
        if s.name[0] is start_letter:
            has_started = True

#    for s in stdt_list:
#        grade_student(s)
    Parallel(n_jobs=4, backend='threading')(delayed(
        grade_student)(s) for s in stdt_list)
