"""
Some helper functions for file organization

Matthew Gee
January, 2017
"""

from collections import namedtuple
import configparser
import contextlib
import datetime
import glob
import os
import re
import shutil
import zipfile

import tqdm

from grading_scripts.student_list import STUDENT_LIST
from utils import cmd_utils


class DirectoryNotFound(OSError):
    pass


class StudentNotFound(LookupError):
    pass


StudentPresentMissing = namedtuple('StudentPresentMissing', 'student present missing')
DirectoryFilenameTimestamp = namedtuple('DirectoryFilenameTimestamp', 'directory filename timestamp')


def zipdir(path, ziph):
    """Zips a directory


    Taken from StackOverflow
    """
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))


def join_zip(assign_num, num_partitions):
    partitions = get_partitions(num_partitions)
    for (first, last) in partitions:
        zipf = zipfile.ZipFile(f'asgt0{assign_num}-finished-{first}-{last}.zip', 'r', zipfile.ZIP_DEFLATED)
        zipf.extractall()


def zip_students(assign_num, start_name, end_name, zip_name=None, progress=None):
    if not zip_name:
        zip_name = f'asgt0{assign_num}-{start_name}-{end_name}.zip'

    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        folder_name = f'asgt0{assign_num}-ready'

        try:
            cur_progress, total_progress = progress
        except TypeError:
            cur_progress, total_progress = 1, len(STUDENT_LIST)

        for (name, email, section) in STUDENT_LIST:
            cmd_utils.progress(cur_progress, total_progress, name)
            if start_name <= name <= end_name:
                zipdir(os.path.join(folder_name, name), zipf)
            cur_progress += 1

    return cur_progress


def get_partitions(num_partitions):
    num_students = len(STUDENT_LIST)

    num_students_partition = int(num_students/num_partitions)
    num_extra = num_students % num_partitions

    current_idx = 0
    partitions = []
    for i in range(num_extra):
        first_student = STUDENT_LIST[current_idx][0]
        last_student = STUDENT_LIST[current_idx + num_students_partition][0]
        partitions.append((first_student, last_student))

        current_idx = current_idx + num_students_partition + 1

    for i in range(num_partitions - num_extra):
        first_student = STUDENT_LIST[current_idx][0]
        last_student = STUDENT_LIST[current_idx + num_students_partition - 1][0]

        partitions.append((first_student, last_student))
        current_idx = current_idx + num_students_partition

    return partitions


def partition_assignment(assign_num, num_partitions):
    num_students = len(STUDENT_LIST)
    print(f'Zipping Assignment {assign_num}')
    partitions = get_partitions(num_partitions)

    zip_dir = f'asgt0{assign_num}-dist'
    if not os.path.exists(zip_dir):
        os.makedirs(zip_dir)

    cur_progress = 1
    total_progress = num_partitions * num_students
    for (first_student, last_student) in partitions:
        cur_progress = zip_students(
            assign_num,
            first_student,
            last_student,
            os.path.join(zip_dir, f'asgt0{assign_num}-{first_student}-last_student.zip'),
            (cur_progress, total_progress)
        )


def get_files(assign_num):
    """ Returns the files associated with each assignment

    assign_num:  which assignment number
    """
    config = configparser.ConfigParser()
    config.read(os.path.join('CS52-GradingScripts', f'asgt0{assign_num}', 'config.ini'))
    files = config['Assignment']['Files'].split(',')
    return files


def check_assignment(assign_number):
    """ Checks the integrity of an assignment's files

    assign_number:  assignment number
    """
    return check_files(get_files(assign_number), f'asgt0{assign_numer}-ready')


def check_files(files, file_dir, student_list=STUDENT_LIST):
    """ Checks the files to see which ones have the necessary files

    files:          files to look for
    file_dir:       where to look
    """
    file_list = []
    for (directory, sub_dirs, sub_files) in os.walk(file_dir):
        if any([os.path.basename(directory) == a for (a, b, c) in student_list]):
            files_present = []
            files_missing = []
            for f in files:
                a = os.path.basename(directory)
                if f'{a}-{f}' in sub_files:
                    files_present.append(f'{a}-{f}')
                else:
                    files_missing.append(f'{a}-{f}')
            file_list.append((directory, {'present': files_present, 'missing': files_missing}))
    return file_list


def get_files_missing(file_list):
    """ Flattens the list of tuples into a readable list on which files are missing

    file_list:      list of tuples returned by check_files()
    """
    return_list = []
    for (directory, files) in file_list:
        for f in files['missing']:
            return_list.append(f)
    return return_list


def get_files_present(file_list):
    """ Flattens the list of tuples into a readable list on which files are missing

    file_list:      list of tuples returned by check_files()
    """
    return_list = []
    for (directory, files) in file_list:
        for f in files['present']:
            return_list.append(f)
    return return_list


def anyCase(st):
    """ Returns glob string

    st:            string to glob
    """
    return ''.join([f'[{c.lower()}{c.lower()}]' if c.isalpha() else c for c in st])


def refresh_file(assign_num, student_name, student_list=STUDENT_LIST):
    """ Updates the files for a particular student

    assign_number:  which assignment
    student_name:   which student
    """
    if not type(student_name) is tuple:
        for (name, email, section) in student_list:
            if name == student_name:
                student_name = (name, email, section)
                break
    files = get_files(assign_num)
    src_dir = f'asgt0{assign_num}-submissions'
    tgt_dir = f'asgt0{assign_num}-ready'
    return move_files(files, src_dir, tgt_dir, [student_name])


def validate_source_dir_exists(source_dir):
    if not os.path.exists(source_dir):
        if re.match('(asgt0)([1-9]{1})(-submissions)', source_dir) is None:
            raise FileNotFoundError("Source Destination doesn't exist")
        raise FileNotFoundError('No submission folder found for given assignment')


def ensure_destination_dir(target_dir):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)


def move_files(files, source_dir, target_dir, overwrite=False, stdt_list=STUDENT_LIST):
    """ Moves students' files from source to target dir

    files:          which files to move
    source_dir:     where to look
    target_dir:     where to move
    stdt_list:      list of students
    """

    validate_source_dir_exists(source_dir)
    ensure_destination_dir(target_dir)

    return_list = []

    for (student, email, section) in tqdm(stdt_list, desc='gathering files'):
        possible_files = glob.glob(os.path.join(source_dir, '*' + anyCase(email) + '*'))
        if not len(possible_files):
            return_list.append(StudentPresentMissing(student, [], files))
        file_list = []
        # possible matches
        for result in possible_files:
            if '2016' not in result and '2017' not in result:
                continue
            if 'latest' in result or 'ontime' in result:
                continue
            submission_time = datetime.datetime.strptime(
                result,
                os.path.join(source_dir, '%Y-%m-%dT%H+%M+%S+%f' + result[result.find('Z'):])
            )

            for (dirpath, dirnames, filenames) in os.walk(result):
                for f in filenames:
                    with contextlib.suppress(Exception):
                        new_file_list = []
                        found = False
                        # for each of the files we've found for for this student
                        for (cur_path, file_name, timestamp) in file_list:
                            # if it matches the name
                            if file_name == f:
                                # if the new one is older keep the previous one
                                if submission_time < timestamp:
                                    new_file_list.append(DirectoryFilenameTimestamp(cur_path, file_name, timestamp))
                                else:
                                    # keep the one we just found
                                    new_file_list.append(DirectoryFilenameTimestamp(dirpath, f, submission_time))
                                found = True
                                # if it doesn't match, keep the old no matter what
                            else:
                                new_file_list.append(DirectoryFilenameTimestamp(cur_path, file_name, timestamp))
                        if not found:
                            new_file_list.append(DirectoryFilenameTimestamp(dirpath, f, submission_time))

                        file_list = new_file_list

        present_list = []
        missing_list = []
        file_tgt_dir = os.path.join(target_dir, student)

        # Copy each file.  Create the dir
        if not os.path.exists(file_tgt_dir):
            os.makedirs(file_tgt_dir)

        # For each file copy it over
        with open(os.path.join(file_tgt_dir, '.timestamps.txt'), 'w+') as f:
            for (d, n, t) in file_list:
                # Adjust for PST
                time = t - datetime.timedelta(hours=8)
                file_src_name = os.path.join(d, n)
                file_tgt_name = os.path.join(file_tgt_dir, f'{student}-{n}')
                present_list.append(n)
                f.write(f'{n},{datetime.datetime.strftime(time, "%Y-%m-%d %H:%M:%S")}\n')
                # If the overwrite flag isn't True, check before copy
                if not overwrite:
                    if not os.path.exists(file_tgt_name):
                        shutil.copy(file_src_name, file_tgt_name)
                else:
                    os.remove(file_tgt_name)
                    shutil.copy(file_src_name, file_tgt_name)

        # Get all the missing files
        for f in files:
            if not any(n == f for (d, n, t) in file_list):
                missing_list.append(f)

        # Format
        return_list.append(StudentPresentMissing(student, present_list, missing_list))

    return return_list
