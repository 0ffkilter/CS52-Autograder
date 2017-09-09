from typing import Text, Optional
from os import path


class Problem:

    def __init__(
        self, assignment_number: int, problem_number: Text,
        number_points: int, number_tests: int, mode: Text = "sml",
        flag: Optional[Text] = None,
        default_path: Text = path.join("grading_scripts", "assignments")
    ):

        self.assignment_number
        self.problem_number = problem_number
        self.points = number_points
        self.tests = number_tests
        self.mode = mode
        self.default_path = default_path
        self.flag = flag
        if self.flag is None:
            self.get_flag()
        self.find_file()

    def find_file(self):
        """
        Finds the path to the test file that's associated with it
        """
        new_path = path.join(
            self.default_path,
            f"asgt0{self.default_path}",
            f"asgt0{self.assignment_number}_{self.problem_number}.{self.mode}"
        )
        self.test_path = new_path

    def get_flag(self):
        """
        TODO: Refactor
        """
        flag = ""
        if len(self.problem_number) > 1:
            if self.problem_number[-1].isalpha():
                if int(self.problem_number[:-1]) < 10:
                    flag = "0%i_0%s" % (self.assignment_number,
                                        self.problem_number)
                else:
                    flag = "0%i_%s" % (self.assignment_number,
                                       self.problem_number)
            else:
                flag = "0%i_%s" % (self.assignment_number,
                                   self.problem_number)
        else:
            if int(self.problem_number) < 10:
                flag = "0%i_0%s" % (self.assignment_number,
                                    self.problem_number)
            else:
                flag = "0%i_%s" % (self.assignment_number,
                                   self.problem_number)

        self.flag = flag
