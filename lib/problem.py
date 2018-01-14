from typing import Text, Optional
from os import path
from lib.constants import *


def get_name(assignment_number: int) -> Text:
    if assignment_number < 10:
        return f"asgt0{assignment_number}"
    else:
        return f"asgt{assignment_number}"


class Problem:

    def __init__(self, assignment_number: int,
                 problem_number: Text, config: dict):

        self.assignment_number = assignment_number
        self.problem_number = problem_number
        self.points = float(config["Points"])
        self.name = config["Name"]
        self.default_path = DEFAULT_GRADING_PATH
        self.tests = 1


class SMLProblem(Problem):

    def __init__(self, assign_number: int, problem_number: Text, config: dict):
        Problem.__init__(self, assign_number, problem_number, config)
        self.mode = "sml"
        if "Flag" in config:
            self.flag = f'0{self.assignment_number}_{config["Flag"]}'
        else:
            self.get_flag()
        self.find_file()
        self.tests = int(config["Tests"])

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

    def find_file(self):
        """
        Finds the path to the test file that's associated with it
        """
        name = get_name(self.assignment_number)
        new_path = path.join(
            self.default_path,
            name,
            f"{name}_{self.problem_number}.{self.mode}"
        )
        self.test_path = new_path


class A52Problem(Problem):

    def __init__(self, assign_number: int, problem_number: Text, config: dict):
        Problem.__init__(self, assign_number, problem_number, config)
        self.answer = config["Answer"]
        self.test_path = path.join(
            self.default_path,
            get_name(assign_number),
            config["Name"]
        )
        self.filename = config["File"]
        self.mode = "a52"
        self.tests = 1


class A52DirectProblem(Problem):

    def __init__(self, assign_number: int, problem_number: Text, config: dict):
        Problem.__init__(self, assign_number, problem_number, config)
        for k, v in config.items():
            print(k, v)
        self.answer = config["Answer"]
        self.input = config["Input"]
        self.runfile = config["File"]
        self.mode = "a52_direct"
        self.tests = 1


class SML_A52Problem(Problem):
    def __init__(self, assign_number: int, problem_number: Text, config: dict):
        Problem.__init__(self, assign_number, problem_number, config)
        self.answer = config["Answer"]
        self.mode = "sml_a52"
        if "Flag" in config:
            self.flag = f'0{self.assignment_number}_{config["Flag"]}'
        else:
            self.get_flag()
        new_path = path.join(
            self.default_path,
            get_name(assign_number),
            f"{get_name(assign_number)}_{self.problem_number}.sml"
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


class JFlapProblem(Problem):
    def __init__(self, assign_number: int, problem_number: Text, config: dict):
        Problem.__init__(self, assign_number, problem_number, config)
        self.tests = int(config["Tests"])
        self.mode = "jflap"
        self.find_file()

    def find_file(self):
        """
        Finds the path to the test file that's associated with it
        """
        name = get_name(self.assignment_number)
        new_path = path.join(
            self.default_path,
            name,
            f"{name}_{self.problem_number}.txt"
        )
        self.test_path = new_path


class VisualProblem(Problem):
    def __init__(self, assign_number: int, problem_number: Text, config: dict):
        Problem.__init__(self, assign_number, problem_number, config)
        self.mode = "visual"

def problem_builder(assign_number: int, problem_number: Text,
                    assign_mode: Optional[Text], config: dict) -> Problem:
    prob_mode = "sml"

    if assign_mode is not None:
        prob_mode = assign_mode

    if "Mode" in config:
        prob_mode = config["Mode"]

    if prob_mode == "sml":
        return SMLProblem(assign_number, problem_number, config)
    elif prob_mode == "a52":
        return A52Problem(assign_number, problem_number, config)
    elif prob_mode == "a52_direct":
        return A52DirectProblem(assign_number, problem_number, config)
    elif prob_mode == "sml_a52":
        return SML_A52Problem(assign_number, problem_number, config)
    elif prob_mode == "visual":
        return VisualProblem(assign_number, problem_number, config)
    elif prob_mode == "jflap":
        return JFlapProblem(assign_number, problem_number, config)
    else:
        print("unknown value")
