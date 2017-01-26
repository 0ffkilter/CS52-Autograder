"""Zips a section of files in an assignment

Usage: 
python checkout_files <assign_num> <start_name> <end_name>


both start_name and end_name are included
"""
import sys
from file_utils import zip_students

if __name__ == '__main__':
	assign_num = int(sys.argv[1])
	start_name = sys.argv[2]
	end_name = sys.argv[3]
	zip_students(assign_num, start_name, end_name)






