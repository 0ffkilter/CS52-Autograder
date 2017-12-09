"""
Some helper functions for file organization

Matthew Gee
January, 2017
"""

import os
import shutil
import glob
import time
import datetime
from utils import cmd_utils
import re
import configparser
import zipfile
from grading_scripts.data.student_list import STUDENT_LIST
from lib.student import Student
from typing import List
from numpy import array_split


REZIP_CODE = """
import zipfile
import os
FIRST="%s"
LAST="%s"
ASSIGN_NUM=%i
def zipdir(path, zipf):
    for root, dirs, files in os.walk(path):
        for f in files:
            zipf.write(os.path.join(root, f))
zipf = zipfile.ZipFile("asgt0" + str(ASSIGN_NUM) + "-finished-" + FIRST + "-" + LAST + ".zip", 'w', zipfile.ZIP_DEFLATED)
zipdir('asgt0' + str(ASSIGN_NUM) + '-ready', zipf)
zipf.close()
"""



#Directory Error
class DirectoryNotFound(OSError):
    pass

#Student Error
class StudentNotFound(LookupError):
    pass


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
        zipf = zipfile.ZipFile('asgt0%i-finished-%s-%s.zip' %(assign_num, first, last), 'r', zipfile.ZIP_DEFLATED)
        zipf.extractall()

def zip_students(assign_num, start_name, end_name, zip_name=None, progress=None):
    zipf = None
    if zip_name is None:
        zipf = zipfile.ZipFile('asgt0%i-%s-%s.zip' %(assign_num, start_name, end_name), 'w', zipfile.ZIP_DEFLATED)
    else:
        zipf = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)


    folder_name = "asgt0%i-ready" %assign_num

    cur_progress = 0
    total_progress = 0

    if progress is None:
        cur_progress = 1
        total_progress = len(STUDENT_LIST)
    else:
        cur_progress, total_progress = progress
    for (name, email, section) in STUDENT_LIST:
        cmd_utils.progress(cur_progress, total_progress, name)
        if (name >= start_name) and (name <= end_name):
            zipdir(os.path.join(folder_name, name), zipf)
        cur_progress = cur_progress + 1

    zipf.close()
    return cur_progress


def get_partitions(num_partitions: int, student_list: List[Student]) -> List[List[Student]]:
    num_students = len(STUDENT_LIST)

    num_students_partition = int(num_students/num_partitions)
    num_extra = num_students % num_partitions

    current_idx = 0
    partitions = []
    for i in range(num_extra):
        first_student= STUDENT_LIST[current_idx][0]
        last_student = STUDENT_LIST[current_idx + num_students_partition][0]
        partitions.append((first_student, last_student))

        current_idx = current_idx + num_students_partition + 1

    for i in range(num_partitions - num_extra):
        first_student= STUDENT_LIST[current_idx][0]
        last_student = STUDENT_LIST[current_idx + num_students_partition -1 ][0]

        partitions.append((first_student, last_student))
        current_idx = current_idx + num_students_partition

    return partitions


def partition_assignment(assign_num, num_partitions):
    num_students = len(STUDENT_LIST)
    print("Zipping Assignment %i" %(assign_num))
    partitions = get_partitions(num_partitions)

    zip_dir = "asgt0%i-dist" %(assign_num)
    if not os.path.exists(zip_dir):
                os.makedirs(zip_dir)

    cur_progress = 1
    total_progress = num_partitions * num_students
    for (first_student, last_student) in partitions:
        cur_progress = zip_students(assign_num,
            first_student, last_student,
            os.path.join(zip_dir, "asgt0%i-%s-%s.zip" %(assign_num, first_student, last_student)),
            (cur_progress, total_progress))


def get_files(assign_num):
    """ Returns the files associated with each assignment

    assign_number:  which assignment number
    """
    config = configparser.ConfigParser()
    config.read(os.path.join("CS52-GradingScripts", "asgt0%i" %(assign_num), "config.ini"))
    files = config["Assignment"]["Files"].split(",")
    return files

def check_assignment(assign_number):
    """ Checks the integrity of an assignment's files

    assign_number:  assignment number
    """
    return check_files(get_files(assign_number), "asgt0%i-ready" %(assign_number))

def check_files(files, file_dir, student_list=STUDENT_LIST):
    """ Checks the files to see which ones have the necessary files

    files:          files to look for
    file_dir:       where to look
    """
    file_list = []
    for (directory, sub_dirs, sub_files) in os.walk(file_dir):
        if any([os.path.basename(directory) == a for (a,b,c) in student_list]):
            files_present = []
            files_missing = []
            for f in files:
                a = os.path.basename(directory)
                if "%s-%s" %(a, f) in sub_files:
                    files_present.append("%s-%s" %(a, f))
                else:
                    files_missing.append("%s-%s" %(a, f))
            file_list.append((directory, {"present":files_present, "missing":files_missing}))
    return file_list


def get_files_missing(file_list):
    """ Flattens the list of tuples into a readable list on which files are missing

    file_list:      list of tuples returned by check_files()
    """
    return_list = []
    for (directory, files) in file_list:
        for f in files["missing"]:
            return_list.append(f)
    return return_list


def get_files_present(file_list):
    """ Flattens the list of tuples into a readable list on which files are missing

    file_list:      list of tuples returned by check_files()
    """
    return_list = []
    for (directory, files) in file_list:
        for f in files["present"]:
            return_list.append(f)
    return return_list

"""
def gather_assignment(assign_number, overwrite=False, student_list=student_list.STUDENT_LIST):
    Gathers the assignment files into asgt0N-ready

    assign_number:  which assignment
    student_list:   list of kiddos

    files = get_files(assign_number)
    src_dir = "asgt0%i-submissions" %(assign_number)
    tgt_dir = "asgt0%i-ready" %(assign_number)
    return move_files(files, src_dir, tgt_dir, overwrite, student_list)
"""


def anyCase(st) :
    """ Returns glob string

    st:            string to glob
    """
    return "".join(["[%s%s]" %(c.lower(), c.upper()) if c.isalpha() else c for c in st])


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
    src_dir = "asgt0%i-submissions" %(assign_num)
    tgt_dir = "asgt0%i-ready" %(assign_num)
    return move_files(files, src_dir, tgt_dir, [student_name])


def move_files(files, source_dir, target_dir, overwrite=False, stdt_list=STUDENT_LIST):
    """ Moves students' files from source to target dir

    files:          which files to move
    source_dir:     where to look
    target_dir:     where to move
    stdt_list:      list of students
    """

    print(f"source: {source_dir}")
    print(files)
    if not os.path.exists(source_dir):
        if re.match("(asgt0)([1-9]{1})(-submissions)", source_dir) is None:
            raise FileNotFoundError("Source Destination doesn't exist")
        else:
            raise FileNotFoundError("No submission folder found for given assignment")


    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        created = False

    return_list = []
    cur_student = 1
    total_students = len(stdt_list)
    for (student, alias, email, section) in stdt_list:

        cmd_utils.progress(cur_student, total_students, email)
        cur_student = cur_student + 1
        #print("%s : %s" %(student, email))
        possibleFiles = glob.glob(os.path.join(source_dir, "*" + anyCase(alias) + "*"))
        if len(possibleFiles) == 0:
            return_list.append((student, [], files))
        file_list = []
        #possible matches
        for result in possibleFiles:


            if "2016" in result or "2017" in result:
                if not 'latest' in result and not 'ontime' in result:
                    #strip the time
                    time = datetime.datetime.strptime(result, os.path.join(source_dir, "%Y-%m-%dT%H+%M+%S+%f" + result[result.find("Z"):]))

                    #Now, for each of the files in there
                    for (dirpath, dirnames, filenames) in os.walk(result):
                        for f in filenames:
                            #if it's one of the files we're looking for
                            content = ""
                            try:
                                #with open(os.path.join(dirpath, f), 'r') as f_temp:
                                #    content = f_temp.read()
                                #if  dirpath.count("-") == 4 or (student in content[:100]) or student[:-1] in content[:100]:

                                idx = dirpath.find("Z-") + 2
                                student_id = dirpath[idx:].split("-")[0]
                                #get the student id
                                new_file_list = []
                                found = False
                                #for each of the files we've found for for this student
                                for (cur_path, file_name, timestamp) in file_list:
                                    #if it matches the name
                                    if file_name == f:
                                        #if the new one is older keep the previous one
                                        if time < timestamp:
                                            new_file_list.append((cur_path, file_name,timestamp))
                                        else:
                                            #keep the one we just found
                                            new_file_list.append((dirpath, f, time))
                                        found = True
                                        #if it doesn't match, keep the old no matter what
                                    else:
                                        new_file_list.append((cur_path, file_name, timestamp))
                                if not found:
                                    new_file_list.append((dirpath, f, time))

                                file_list = new_file_list
                                #else:
                                #    print("failed check")
                            except:
                                pass


        present_list = []
        missing_list = []
        file_tgt_dir = os.path.join(target_dir, student)


        #Copy each file.  Create the dir
        if not os.path.exists(file_tgt_dir):
            os.makedirs(file_tgt_dir)

        #For each file copy it over
        with open(os.path.join(file_tgt_dir, ".timestamps.txt"), 'w+') as f:
            for (d, n, t) in file_list:

                #Adjust for PST
                time = t - datetime.timedelta(hours=8)
                file_src_name = os.path.join(d,n)
                file_tgt_name = os.path.join(file_tgt_dir, "%s-%s" %(student, n))
                present_list.append(n)
                f.write("%s,%s\n" %(n,datetime.datetime.strftime(time, "%Y-%m-%d %H:%M:%S")))
                #If the overwrite flag isn't True, check before copy
                if not overwrite:
                    if not os.path.exists(file_tgt_name):
                        shutil.copy(file_src_name, file_tgt_name)

                else:
                    if os.path.exists(file_tgt_name):
                        os.remove(file_tgt_name)
                    shutil.copy(file_src_name, file_tgt_name)


        #Get all the missing files
        for f in files:
            found = False
            for (d, n, t) in file_list:
                if n == f:
                    found = True
            if not found:
                missing_list.append(f)

        #Format
        return_list.append((student, present_list, missing_list))

    return return_list


