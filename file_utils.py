"""
Some helper functions for file organization

Matthew Gee
January, 2017
"""

import os
import shutil
import glob
from config import ASSIGNMENT_FILES
import time
import datetime
from grading_scripts import student_list
import re


#Directory Error
class DirectoryNotFound(OSError):
    pass    

#Student Error
class StudentNotFound(LookupError):
    pass


def get_files(assign_number):
    """ Returns the files associated with each assignment

    assign_number:  which assignment number
    """
    return ASSIGNMENT_FILES.get(assign_number, None)

def check_assignment(assign_number):
    """ Checks the integrity of an assignment's files

    assign_number:  assignment number
    """
    return check_files(get_files(assign_number), "asgt0%i-ready" %(assign_number))

def check_files(files, file_dir, student_list=student_list.STUDENT_LIST):
    """ Checks the files to see which ones have the necessary files

    files:          files to look for
    file_dir:       where to look
    """
    file_list = []
    for (directory, sub_dirs, sub_files) in os.walk(file_dir):
        print(directory)
        print(os.path.basename(directory))
        if any([os.path.basename(directory) == a for (a,b,c) in student_list]):
            print("foo")
            files_present = []
            files_missing = []
            for f in files:
                if f in sub_files:
                    files_present.append(f)
                else:
                    files_missing.append(f)
            file_list.append((directory, {"present":files_present, "missing":files_missing}))
    return file_list


def get_files_missing(file_list):
    """ Flattens the list of tuples into a readable list on which files are missing

    file_list:      list of tuples returned by check_files()
    """
    return_list = []
    for (directory, files) in file_list:
        for f in files["missing"]:
            return_list.append(os.path.join(directory, f))
    return return_list


def get_files_present(file_list):
    """ Flattens the list of tuples into a readable list on which files are missing

    file_list:      list of tuples returned by check_files()
    """
    return_list = []
    for (directory, files) in file_list:
        for f in files["present"]:
            return_list.append(os.path.join(directory, f))
    return return_list


def gather_assignment(assign_number, student_list=student_list.STUDENT_LIST):
    """ Gathers the assignment files into asgt0N-ready

    assign_number:  which assignment
    student_list:   list of kiddos
    """
    files = get_files(assign_number)
    src_dir = "asgt0%i-submissions" %(assign_number)
    tgt_dir = "asgt0%i-ready" %(assign_number)
    move_files(files, src_dir, tgt_dir, student_list)


def anyCase(st) :
    """ Returns glob string

    st:            string to glob
    """
    return "".join(["[%s%s]" %(c.lower(), c.upper()) if c.isalpha() else c for c in st])


def refresh_file(assign_number, student_name, student_list=student_list.STUDENT_LIST):
    """ Updates the files for a particular student

    assign_number:  which assignment
    student_name:   which student
    """
    if not type(student_name) is tuple:
        for (name, email, section) in student_list:
            if name == student_name:
                student_name = (name, email, section)
                break
    files = get_files(assign_number)
    src_dir = "asgt0%i-submissions" %(assign_number)
    tgt_dir = "asgt0%i-ready" %(assign_number)
    move_files(files, src_dir, tgt_dir, [student_name])
    

def move_files(files, source_dir, target_dir, stdt_list=student_list.STUDENT_LIST):
    """ Moves students' files from source to target dir 

    files:          which files to move
    source_dir:     where to look
    target_dir:     where to move
    stdt_list:      list of students
    """
    if not os.path.exists(source_dir):
        if re.match("(asgt0)([1-9]{1})(-submissions)", source_dir) is None:
            raise FileNotFoundError("Source Destination doesn't exist")
        else:
            raise FileNotFoundError("No submission folder found for given assignment")


    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        created = False

    return_list = []
    for (student, email, section) in stdt_list:
        print("%s : %s" %(student, email))
        possibleFiles = glob.glob(os.path.join(source_dir, "*" + anyCase(email) + "*"))
        if len(possibleFiles) == 0:
            return_list.append((student, []))
            print("\tNo Submission")

        file_list = []

        #possible matches
        for result in possibleFiles:
            if "2016" in result:
                #strip the time
                time = datetime.datetime.strptime(result, os.path.join(source_dir, "%Y-%m-%dT%H+%M+%S+%f" + result[result.find("Z"):]))

                #Now, for each of the files in there
                for (dirpath, dirnames, filenames) in os.walk(result):
                    for f in filenames:
                        #if it's one of the files we're looking for
                        if f in files:
                            #get the student id
                            student_id = dirpath.split("-")[-1]
                            new_file_list = []
                            found = False
                            #for each of the files we've found for for this student
                            for (cur_path, file_name, timestamp) in file_list:
                                #if it matches the name
                                if file_name == f:
                                    #if the new one is older keep the previous one
                                    if time > timestamp:
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

        #okay, so now file_list contains triples of (directory, name, time) - time to record the missing ones

        present_list = []
        missing_list = []
        file_tgt_dir = os.path.join(target_dir, student)

        if not os.path.exists(file_tgt_dir):
            os.makedirs(file_tgt_dir)
        for (d, n, t) in file_list:
            file_src_name = os.path.join(d,n)
            file_tgt_name = os.path.join(file_tgt_dir, "%s-%s" %(student, n))
            present_list.append(n)
            if not os.path.exists(os.path.join(file_tgt_name)):
                shutil.copy(file_src_name, file_tgt_name)


        for f in files:
            found = False
            for (d, n, t) in file_list:
                if n == f:
                    found = True
            if not found:
                missing_list.append(f)
        return_list.append((student, present_list, missing_list))
    return return_list

  
gather_assignment(4)
print(get_files_missing(check_assignment(4)))