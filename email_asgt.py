from lib.gmailer import GoogleMailer
from grading_scripts.data.student_list import STUDENT_LIST
from typing import Text
from os.path import join, exists
from time import sleep

mailer = GoogleMailer()

assignment_number = 5


def discover_file(student: Text, assignment: int, filename: Text) -> Text:

    path = join("assignments", f"asgt0{assignment}",
                f"asgt0{assignment}-finished", student)
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

Sorry for the delay - I'm just a senior who doesn't have his shit together.  

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
        except Exception as e:
            print(e)
