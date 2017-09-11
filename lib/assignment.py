
import configparser
from lib.problem import Problem
from typing import Text, Optional
from os import path
from collections import OrderedDict

DEFAULT_GRADING_PATH = path.join("grading_scripts", "assignments")

class Assignment:

    def __init__(self, assignment_number: int,
                 grading_path: Text = DEFAULT_GRADING_PATH):

        config_file = path.join(grading_path,
                                f"asgt0{assignment_number}",
                                "config.ini")

        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.grading_path = grading_path
        self.assignment_number = assignment_number
        self.due_date = self.config["Assignment"]["DueDate"]
        self.total_points = int(self.config["Assignment"]["TotalPoints"])
        self.style_points = int(self.config["Assignment"]["StylePoints"])
        self.num_problems = int(self.config["Assignment"]["NumProblems"])
        self.problem_points = self.total_points - self.style_points
        self.problems = OrderedDict()
        self.files = self.config["Assignment"]["Files"].split(",")
        if len(self.files) is 1:
            self.file = self.files[0]
        if "Mode" in self.config["Assignment"]:
            self.mode = self.config["Assignment"]["Mode"]
        else:
            self.mode = "sml"
        if self.mode is "sml":
            self.solution_path = path.join(grading_path,
                                           f"asgt0{assignment_number}",
                                           "resources",
                                           f"asgt0{assignment_number} \
                                           _solution.sml")
        else:
            self.solution_path = None

        self.build_problems()

    def next_problem(self, problem_number: Optional[Text]):
        """
        Returns the next problem in the ordered Dict, or
        None if it's an index error :(
        """
        if problem_number is None:
            return list(self.problems.items())[0][0]
        try:
            new_idx = [list(self.problems.keys()).index(problem_number) + 1][0]
            return list(self.problems.items())[new_idx]
        except IndexError:
            return None

    def build_problems(self):
        """
        Returns a list of triples of problems
        [(problem_name, problem_type, data)]


        """
        for i in range(1, self.num_problems + 1):
            cur_mode = self.mode
            cur_num = str(i)

            if "Problems" in self.config[cur_num]:
                for sub_problem in self.config[cur_num]["Problems"].split(","):
                    cur_prob = f"{cur_num}{sub_problem}"
                    if "Mode" in self.config[cur_prob]:
                        cur_mode = self.config[cur_prob]["Mode"]
                    self.problems[cur_prob] = Problem(
                        self.assignment_number,
                        cur_prob,
                        self.config[cur_prob]["Name"],
                        float(self.config[cur_prob]["Points"]),
                        int(self.config[cur_prob]["Tests"]),
                        cur_mode)

            else:
                self.problems[cur_num] = Problem(
                    self.assignment_number,
                    cur_num,
                    self.config[cur_num]["Name"],
                    float(self.config[cur_num]["Points"]),
                    int(self.config[cur_num]["Tests"]),
                    cur_mode)
