from typing import Text, List, Optional
import configparser
from problem import Problem
from os import path
from collections import OrderedDict

class Assignment:
    def __init__(self, assignment_number: int, grading_path: Text = "grading_scripts"):

        config_file = path.join(grading_path, f"asgt0{assignment_number}", "config.ini")

        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.grading_path = grading_path
        self.assignment_number = assignment_number
        self.due_date = config["Assignment"]["DueDate"]
        self.total_points = int(config["Assignment"]["TotalPoints"])
        self.style_points = int(config["Assignment"]["StylePoints"])
        self.num_problems = int(config["Assignment"]["NumProblems"])
        self.problem_points = total_points - style_points 
        self.problems = OrderedDict()
        if "Mode" in config["Assignment"]:
            self.mode = config["Assignment"]["Mode"]
        else:
            self.mode = "sml"
        if self.mode is "sml":
            self.solution_path = path.join(grading_path, f"asgt0{assignment_number}", "resources", f"asgt0{assignment_number}_solution.sml")
        else:
            self.solution_path = None

        self.build_problems()

    def next_problem(self, problem_number: Optional[Text]):
        """
        Returns the next problem in the ordered Dict, or None if it's an index error :(
        """
        if problem_number is None:
            return list(self.problems.items())[0][0]
        try:
            return list(self.problems.items())[list(self.problems.keys()).index(problem_number) + 1][0]
        except IndexError:
            return None

    def build_problems(self):
        """
        Returns a list of triples of problems
        [(problem_name, problem_type, data)]


        """
        for i in range(1, num_problems+1):
            cur_mode = self.mode
            cur_num = str(i)

            if "Problems" in self.config[cur_num]:
                for sub_problem in config[cur_num]["Problems"].split(","):
                    cur_prob = f"{cur_num}{sub_problem}"
                    if "Mode" in config[cur_prob]:
                        cur_mode = config[cur_prob]["Mode"]
                    self.problems[cur_prob] = Problem(self.assignment_number,
                                    cur_num,
                                    int(config[cur_num]["Points"]),
                                    int(config[cur_num]["Tests"]),
                                    cur_mode)       
            else:
                self.problems[cur_num] = Problem(self.assignment_number,
                                                cur_num,
                                                int(config[cur_num]["Points"]),
                                                int(config[cur_num]["Tests"]),
                                                cur_mode)       
