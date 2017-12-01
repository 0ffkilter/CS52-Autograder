from zipfile import ZipFile, ZIP_DEFLATED
from grading_scripts.data.student_list import STUDENT_LIST
from lib.assignment import Assignment
from lib.student import Student
from os import path, getcwd, mkdir, walk, chdir
from joblib import Parallel, delayed
from utils.file_utils import move_files
from numpy import array_split
from typing import Text, List
from lib.grader_code import REZIP_CODE


def grade_student(s: Student):
    try:
        print(s.name)
        print(s.name)
        s.run_all()
        s.export_results()
    except ConnectionRefusedError:
        pass


def generate_student(s: Student):
    s.initialize()


def zipdir(dir_to_zip: Text, ziph: ZipFile, relpath: Text):
    """Zips a directory


    Taken from StackOverflow
    """
    # ziph is zipfile handle
    for root, dirs, files in walk(dir_to_zip):
        for file in files:
            ziph.write(path.join(root, file))


def package_dist(assignment_path: Text, num_partitions: int,
                 assignment: Assignment, students: List[Student]):
    partitions = array_split(students, num_partitions)
    if not path.exists(path.join(assignment_path,
                                 f"asgt0{assignment.assignment_number}-dist")):
        mkdir(path.join(assignment_path,
                        f"asgt0{assignment.assignment_number}-dist"))

    chdir(assignment_path)
    for p in partitions:
        first = p[0].name
        last = p[-1].name

        dist_zip = ZipFile(path.join(
            f"asgt0{assignment.assignment_number}-dist",
            f"asgt0{assignment.assignment_number}-{first}-{last}.zip"),
            "w",
            ZIP_DEFLATED)
        for s in p:
            zipdir(path.relpath(s.dir), dist_zip, assignment_path)

        with open("rezip.py", "w") as f:
            f.write(REZIP_CODE % (first, last, assignment.assignment_number))

        dist_zip.write("rezip.py")

        dist_zip.close()


if __name__ == '__main__':

    assignment_number = 8
    asgt = Assignment(assignment_number)


    assignment_path = path.join(getcwd(), "assignments", "asgt08")

    gather = True
    generate = True
    grade = True
    package = True

    if gather:
        move_files(asgt.files,
                   path.join(assignment_path, "asgt08-submissions"),
                   path.join(assignment_path, "asgt08-ready"),
                   False,
                   STUDENT_LIST)

    students = []

    default_student_dir = path.join(assignment_path, "asgt08-ready")

    has_started = False

    student_name = None
    port_count = 3000
    for (name, alias, email, section) in STUDENT_LIST:
        print(name)
        if student_name is not None and name != student_name:
            continue
        students.append(Student(
            name,
            alias,
            email,
            section,
            asgt,
            path.join(default_student_dir, name),
            port_count
        ))
        port_count = port_count + 100
    print("len", len(students))

    if generate:
        Parallel(n_jobs=4, backend='threading')(delayed(
            generate_student)(s) for s in students)

    if grade:
        Parallel(n_jobs=4, backend='threading')(delayed(
            grade_student)(s) for s in students)

    if package:
        package_dist(assignment_path, 3, asgt, students)
