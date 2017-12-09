from lib.gmailer import GoogleMailer
from grading_scripts.data.student_list import STUDENT_LIST
from typing import Text
from os.path import join, exists
from time import sleep
from lib.assignment import get_name
import sys

mailer = GoogleMailer()

assignment_number = sys.argv[1]

def discover_file(student: Text, assignment: int, filename: Text) -> Text:
    name = get_name(assignment)
    path = join("assignments", name,
                f"{name}-finished", student)
    if exists(join(path, filename)):
        return join(path, filename)
    return None


for (name, alias, email, section) in STUDENT_LIST:
    file = discover_file(name, assignment_number,
                         f"asgt0{assignment_number}-grades.txt")
    print(name, file is not None)
    message = f"""Hi,
This is your grade from assignment {assignment_number}.

If you have any questions or comments, post on piazza and we'll try our best to help you out!

Also, don't reply to this email - it'll probably take until next semester for me to read it.  Piazza works better.  

Best,

The CS52 TAs
"""
    if file is not None:
        try:
            res = mailer.send_email("cs052grading@gmail.com", email,
                                    f"Assignment {assignment_number} Grades",
                                    message, html=None,
                                    attachment=file)
            sleep(0.1)
        except Exception as e:
            print(e)
