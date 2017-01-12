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


def grade_assignment(assign_num, config):

	#First we gather the files:
	file_list = gather_files(assign_num)

	#Generate list of missing files:


	#write to asgt0N-ready/missing.txt








def main():
	parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)

	parser.add_argument('-grade', action='store', dest='grade', default='-1', type=string, help =
	"""
	Grade the assignment.  Provide assignment number (1,2,etc...) or a student name ("Smith")
	""")

	parser.add_argument('-gather', action='store', dest='grade', default='-1', type=string, help =
	"""
	Gather assignment files (or one student's)
	""")

	parser.add_argument('-check', action='store', dest='check', default='-1', type=string, help =
	"""
	Check integrity of files, or refresh student files.  
	""")

	parser.add_argument('-print', action='store', dest='print', default='-1', type=string, help =
	"""
	Print assignment, or student's files.  
	""")


	res = parser.parse_args()
	print(res)