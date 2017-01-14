#Generates a fake assignment

import os
import random
import datetime
import shutil
import sys
from grading_scripts.student_list import STUDENT_LIST

#January 10, 2017 at 5pm
#Arbitrarily chosen
file_string = "2017-01-10T17+00+00+000Z-%s"

assign_num = int(sys.argv[1])
file = sys.argv[2]

os.makedirs("asgt0%i-submissions" %(assign_num))
for (name, email, section) in STUDENT_LIST:
	os.makedirs(os.path.join("asgt0%i-submissions" %(assign_num), file_string %(email)))
	shutil.copy(file, os.path.join("asgt0%i-submissions" %(assign_num), file_string %(email), "asgt0%i.sml" %(assign_num)))


