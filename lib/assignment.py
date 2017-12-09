import configparser
from lib.problem import Problem, SMLProblem, A52Problem, problem_builder
from typing import Text, Optional
from os import path
from collections import OrderedDict
from lib.constants import DEFAULT_GRADING_PATH

def get_name(assignment_number: int) -> Text:
    if assignment_number < 10:
        return f"asgt0{assignment_number}"
    else:
        return f"asgt{assignment_number}"


class Assignment:

    def __init__(self, assignment_number: int,
                 grading_path: Text = DEFAULT_GRADING_PATH):

        self.name = get_name(assignment_number)
        self.assignment_path = path.join(grading_path,
                                         self.name)
        self.resource_path = path.join(self.assignment_path, "resources")
        config_file = path.join(self.assignment_path, "config.ini")

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
                                           self.name,
                                           "resources",
                                           f"{self.name} \
                                           _solution.sml")
        self.starter_file = None
        if "StarterCode" in self.config["Assignment"]:
            self.starter_file = path.join(
                self.assignment_path,
                self.config["Assignment"]["StarterCode"])
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
            cur_num = str(i)
            if "Problems" in self.config[cur_num]:
                for sub_problem in self.config[cur_num]["Problems"].split(","):
                    cur_prob = f"{cur_num}{sub_problem}"
                    self.problems[cur_prob] = problem_builder(
                        self.assignment_number,
                        cur_prob,
                        self.mode,
                        self.config[cur_prob])
            else:
                self.problems[cur_num] = problem_builder(
                    self.assignment_number,
                    cur_num,
                    self.mode,
                    self.config[cur_num])
