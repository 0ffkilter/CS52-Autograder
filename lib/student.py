from assignment import Assignment
from typing import Text, Optional
from server_handler import ServerHandler
from os import path, mkdir
from collections import OrderedDict


class Student:

    def __init__(self, name: Text, assignment: Assignment, student_dir):
        self.current_problem = "1"
        self.assignment = assignment
        self.dir = student_dir
        self.name = name
        self.port = hash(name) % (10 ** 8)
        self.server = ServerHandler(self.port)
        self.results = OrderedDict()
        self.problems = {}

        self.is_started = False

    def generate_subfiles(self, filename):
        grading_path = path.join(self.dir, "grading")
        if not path.exists(grading_path):
            mkdir(grading_path)
        # fname = f"{self.name}-{filename}"

        with open(filename, 'r') as f:
            file_contents = f.read()

        for k, v in self.assignment.problems.items():
            if v.mode is "sml":
                problem_path = path.join(
                    grading_path,
                    f"asgt0{self.assignment.assignment_number}_{k}.sml"
                )
                with open(grading_path, 'w+') as f:
                    f.write(self.split_string(file_contents, v.flag))
                    self.problems[k] = problem_path

    def start(self):
        if not self.is_started:
            self.server.start()
            self.is_started = True

    def finish(self):
        if self.is_started:
            self.server.kill()
            self.is_started = False

    def parse_test_results(self, test_results: Text):
        """Returns a dict containing some test results

        results[problem_number][test_number] = result
        results[problem_number] = [r0, r1, r2, ...etc] (None if no result)
        """
        results = test_results.split("|")
        for r in results:
            sections = r.split("/")
            problem = sections[0] +  \
                      (sections[1] if sections[1] is not " " else "")
            if problem not in self.results:
                self.results[problem] = [None] * 10
            self.results[problem][int(sections[2])] = int(sections[3])

    def run_problem(self, problem_number: Optional[Text] = None,
                    file: Optional[Text] = None):
        """Runs the file associated with the problem number
        If nothing is specified, runs the next problem
                after the last one previously run
        """
        current_problem = problem_number or self.current_problem
        self.current_problem = self.assignment.next_problem(current_problem)
        self.server.run_file(self.problems[current_problem])

        if current_problem[-1].isalpha():
            self.parse_test_results(
                self.server.get_results(
                    current_problem[:-1], current_problem[-1])
            )
        else:
            self.parse_test_results(self.server.get_results(current_problem))
