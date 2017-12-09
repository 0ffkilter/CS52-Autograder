import argparse
import shutil
from zipfile import ZipFile, ZIP_DEFLATED
from grading_scripts.data.student_list import STUDENT_LIST
from lib.assignment import Assignment, get_name
from lib.student import Student
from os import path, getcwd, mkdir, walk, chdir,removedirs, makedirs
from joblib import Parallel, delayed
from utils.file_utils import move_files
from numpy import array_split
from typing import Text, List
from lib.constants import REZIP_CODE
from sys import exit
from shutil import rmtree


def grade_student(s: Student):
    try:
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
                                 assignment.name)):
        mkdir(path.join(assignment_path,
                        f"{assignment.name}-dist"))

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


    parser = argparse.ArgumentParser(description="Autograde an assignment")

    parser.add_argument("-c", action="store_true", help="Collect student files")
    parser.add_argument("-d", action="store_true", help="Delete the asgt0N-folder and make a new one")
    parser.add_argument("-s", action="store_true", help="Setup files for grading")
    parser.add_argument("-g", action="store_true", help="Grade files that are gathered")
    parser.add_argument("-p", action="store_true", help="Package files for distribution")
    parser.add_argument("-t", action="store_true", help="Generate fake assignment before grading")
    parser.add_argument("-r", action="store_true", help="Regrade any students without a grades.txt")

    parser.add_argument("--student", action="store", dest="student", type=str, default=None, help="Only grade a certain student's files")

    parser.add_argument("--submission-folder", action="store", dest="submit_folder", type=str, default=None,
        help="Point to the submission folder - defaults to asgt0N-submissions")

    parser.add_argument("--grading-folder", action="store", dest="grading_folder", type=str, default=None,
        help="Point to the output folder - defaults to asgt0N-ready")

    parser.add_argument("--num-zips", action="store", dest="num_zips", type=int, default=3, help=
        "Number of zips to package into - default 3")

    parser.add_argument("--num-threads", action="store", dest="num_threads", type=int, default=4, help=
        "Number of threads to use for concurrency - default 4")

    parser.add_argument("assignment", type=int)

    args = parser.parse_args()

    assignment_number = args.assignment

    asgt = Assignment(assignment_number)
    assignment_folder = path.join(getcwd(), "assignments", asgt.name)

    submissions_folder = path.join(assignment_folder, f"{asgt.name}-submissions")

    output_folder = path.join(assignment_folder, f"{asgt.name}-ready")
    
    if args.submit_folder is not None:
        if path.exists(args.submit_folder):
            submissions_folder = args.submit_folder
        else:
            print("Submissions folder does not exist")
            exit(1)


    if path.exists(output_folder):
        if args.d:
            print(f"Removing old folder - {output_folder}")
            rmtree(output_folder)
            mkdir(output_folder)

    else:
        mkdir(output_folder)

    if args.t:
        print("Generating new assignment")
        file_string = "2017-01-10T17+00+00+000Z-%s"

        files = [path.join(asgt.resource_path, f) for f in asgt.files]

        for (name, alias, email, section) in STUDENT_LIST:
            makedirs(path.join(submissions_folder, file_string % (alias)),
                     exist_ok=True)
            for f in files:
                shutil.copy(f, path.join(
                    submissions_folder,
                    file_string % (alias),
                    path.basename(f).replace("-solution", "")))

    student_list = STUDENT_LIST
    if args.student is not None:
        student_list = [(a, b, c, d) for (a, b, c, d) in STUDENT_LIST
                        if a == args.student]

    if args.c:
        print("Collecting Files")
        move_files(asgt.files,
                   submissions_folder,
                   output_folder,
                   True,
                   student_list)

    default_student_dir = path.join(assignment_folder, output_folder)

    port_count = 3000
    students = []
    for (name, alias, email, section) in student_list:
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

    new_student_list = []
    if args.r:
        for s in students:
            if not path.exists(path.join(s.dir, f"{asgt.name}-grades.txt")):
                new_student_list.append(s)
                print(s.name)
        students = new_student_list

    if args.s:
        print("Generating student files")
        Parallel(n_jobs=args.num_threads, backend='threading')(delayed(
            generate_student)(s) for s in students)

    if args.g:
        print("Grading")
        Parallel(n_jobs=args.num_threads, backend='threading')(delayed(
            grade_student)(s) for s in students)

    if args.p:
        package_dist(assignment_folder, args.num_zips, asgt, students)
