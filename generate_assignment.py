"""Generates a fake assignment

Usage:  python generate_assignment.py <assign_number> <file1> <file2> ...

Puts each of the files in asgt0N-submissions/<timestamp>-<name> for each name in student list.

Removes '-solution' from filename for ease of use
"""
import os
import shutil
import sys
from grading_scripts.student_list import STUDENT_LIST

#January 10, 2017 at 5pm
#Arbitrarily chosen
file_string = "2017-01-10T17+00+00+000Z-%s"

assign_num = int(sys.argv[1])
files = sys.argv[2:]

os.makedirs("asgt0%i-submissions" %(assign_num))
for (name, email, section) in STUDENT_LIST:
	os.makedirs(os.path.join("asgt0%i-submissions" %(assign_num), file_string %(email)))
	for f in files:
		shutil.copy(f, os.path.join("asgt0%i-submissions" %(assign_num), file_string %(email), os.path.basename(f).replace("-solution", "")))
