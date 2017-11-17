import socket
from lib.assignment import Assignment
from typing import Text, Optional
from lib.server_handler import ServerHandler
from os import path, makedirs, remove, getcwd
from collections import OrderedDict
from utils.grading_utils import split_string
from utils.cmd_utils import run_a52
from shutil import copy
from http.client import HTTPException
from re import match, DOTALL
from lib.grader_code import RUN_A52

DEFAULT_PATH_TO_ASSERT = path.join("serve-sml", "assert.sml")
DEFAULT_PATH_TO_A52_LIBS = path.join("grading_scripts", "data")
DEFAULT_A52_LIBRARY_FILES = ["divilib.a52", "divrlib.a52", "mullib.a52"]
DEFAULT_PATH_TO_JAR = path.join("grading_scripts", "data", "cs52-machine.jar")


class Student:

    def __init__(self, name: Text, alias: Text, email: Text,
                 section: int, assignment: Assignment, student_dir: Text,
                 port: Optional[int] = None):

        # pointer to linked Assignment Object
        self.assignment = assignment

        # path to student workdir (usually asgt0N-ready/name)
        self.dir = student_dir

        # name of student
        # usually all last name, but will take letters from first name
        # if there are duplicates
        # Justin Lee, Kevin Lee -> LeeJ, LeeK
        self.name = name

        # id@campus from sakai roster
        self.alias = alias

        # email from sakai roster
        self.email = email

        # section number
        self.section = section

        # generated port id from alias
        self.port = hash(alias) % (10 ** 8) if port is None else port

        # ordered dict of test results
        # in format of results[problem_number][test_number]
        self.results = OrderedDict()

        # dict of problem name : file_path (at least for sml)
        self.problems = {}

        # number of servers started, for port iteration
        # TODO: come up with better idea
        self.server_count = 0

        # bool to track if server is up
        # used in case of infinite recursion where
        #   server.check_status() would fail
        self.is_started = False

        # Personalized header for grading file
        self.header = f"""Grades for Assignment {self.assignment.assignment_number}
Name:      {self.name}
UserId:    {self.alias}
Section:   {self.section}
Assignment {self.assignment.assignment_number}

"""

    def generate_subfiles(self, filename: Text):
        """ Generates sml grading subfiles in student_dir/grading

        Keyword Arguments:
        filename:  The sml file to generate subfiles
        """
        # fname = f"{self.name}-{filename}"

        copy(DEFAULT_PATH_TO_ASSERT, self.grading_path)

        file_path = path.join(self.dir, f"{self.name}-{filename}")
        if not path.exists(file_path):
            return

        if path.exists(path.join(self.dir, "server_log.txt")):
            remove(path.join(self.dir, "server_log.txt"))

        with open(file_path, 'r') as f:
            file_contents = f.read()

        default_write_string = ""
        if self.assignment.starter_file is not None:
            copy(self.assignment.starter_file, self.grading_path)
            fname = path.basename(self.assignment.starter_file)
            default_write_string = f"(* use \"{fname}\"; *)\n"
            print(default_write_string)

        for k, v in self.assignment.problems.items():
            print(f"{self.name} generate: {k}")
            if v.mode is "sml":
                print(f"{self.name} generate sml: {k}")
                problem_path = path.join(
                    self.grading_path,
                    f"asgt0{self.assignment.assignment_number}_{k}.sml"
                )
                write_string = default_write_string
                write_string = write_string + "(* use \"assert.sml\"; *)"
                write_string = write_string + split_string(
                    file_contents, v.flag)
                write_string = write_string + \
                    f"\naddTest \"{k}\" \"0\" \"Compilation Test\" \"0\";"

                with open(v.test_path, 'r') as f:
                    content = f.read()
                    write_string = f"{write_string}\n\n{content}"

                with open(problem_path, 'w+') as f:
                    f.write(write_string)
                    self.problems[k] = problem_path
                str_len = len(write_string)
                print(f"{self.name} generate: {k}, {str_len} {problem_path}")

    def a52_initialize(self):
        for f in DEFAULT_A52_LIBRARY_FILES:
            copy(path.join(DEFAULT_PATH_TO_A52_LIBS, f), self.dir)
            copy(path.join(DEFAULT_PATH_TO_A52_LIBS, f), getcwd())

        for k, v in self.assignment.problems.items():
            if v.mode is "a52":
                copy(v.test_path, self.grading_path)

        copy(DEFAULT_PATH_TO_JAR, self.dir)

    def a52_direct_initialize(self, problem):
        copy(path.join(self.assignment.resource_path, problem.runfile),
             self.grading_path)

    def initialize(self):
        self.grading_path = path.join(self.dir, "grading")
        if not path.exists(self.grading_path):
            makedirs(self.grading_path)

        # Blanket initialization
        if any([v.mode is "sml" for k, v in self.assignment.problems.items()]):
            for f in self.assignment.files:
                self.generate_subfiles(f)
        # Blanket initialization
        if any([v.mode is "a52" for k, v in self.assignment.problems.items()]):
            self.a52_initialize()
            with open(path.join(self.dir, "grader.py"), "w+") as f:
                f.write(RUN_A52.replace("$NAME$", self.name))

        # Per Problem initalization
        for k, v in self.assignment.problems.items():
            if v.mode is "a52_direct":
                self.a52_direct_initialize(v)

        if self.assignment.mode == "circ":
            with open(path.join(
                self.dir,
                f"asgt0{self.assignment.assignment_number}-grades.txt"),
                    "w+") as f:
                f.write(self.header)

    def start(self):
        if not self.is_started:
            self.server = ServerHandler(self.port + self.server_count,
                                        name=self.name,
                                        log_file=path.join(
                                            self.dir, "server_log.txt"))
            self.server_count = self.server_count + 1
            self.server.start()
            self.is_started = True

    def end(self):
        if self.is_started:
            self.server.kill()
            self.is_started = False

    def result_to_string(self, result: int) -> Text:
        return {0: "Pass",
                1: "Fail: Incorrect Answer",
                2: "Fail: Unexpected Error - Test did not run",
                3: "Fail: Unexpected Error - Test failed to complete"
                }.get(result)

    def compilation_string(self, result: int) -> Text:
        return {0: "Sucessful",
                3: "Error Compiling"}.get(result)

    def get_score(self, max_score: float, num_tests: int, num_passed: int):
        # 0 iff no tests passed
        # all if all tests passed
        # -0.5 for each test failed
        if num_passed is 0:
            return 0
        if num_passed is num_tests:
            return max_score
        return max(0, max_score - ((num_tests - num_passed) * 0.5))

    def export_results(self):
        print(self.results)
        end_string = self.header

        total_points = self.assignment.total_points
        style_points = self.assignment.style_points
        assignment_points = total_points + style_points
        total_tests = 0

        tests_passed = 0
        problem_points = 0
        for (p, v) in self.results.items():
            current_problem = self.assignment.problems[p]

            number_points = current_problem.points
            number_tests = current_problem.tests
            total_tests = total_tests + number_tests
            name = current_problem.name
            end_string = f"{end_string}\n\n{p}: {name}\n======"

            if current_problem.mode is "sml":
                r = self.compilation_string(v[0][0])
                end_string = f"{end_string}\n\tCompilation: {r}"
                v = v[1:]

            passed = 0
            for t in range(0, len(v)):
                r, s = v[t]
                res = self.result_to_string(r)
                end_string = f"{end_string}\n\tTest {t}: {res}"
                if r is 1:
                    end_string = f"{end_string}\n\t\t{s}\n"
                if r is 0:
                    passed = passed + 1

            tests_passed = tests_passed + passed
            score = self.get_score(number_points, number_tests, passed)
            end_string = f"{end_string}\n======="
            end_string = f"{end_string}\nPoints: {score}/{number_points}"
            problem_points = problem_points + score

        student_points = problem_points + style_points
        end_string = f"""{end_string}

Results
==============================
Tests Passed:       {tests_passed}/{total_tests}
Correctness Score:  {problem_points}/{total_points}
Style Points:       {style_points}/{style_points}
Total Score:        {student_points}/{assignment_points}
==============================

Grader Comments
==============================










==============================
Questions? Comments? Missed something? Post on Piazza (preferably private)
"""

        with open(path.join(
            self.dir,
            f"asgt0{self.assignment.assignment_number}-grades.txt"),
                "w+") as f:
            f.write(end_string)

    def parse_test_results(self, test_results: Text, problem_number: Text):
        """Returns a dict containing some test results

        Test results are in the format of
        problem_number/sub_p_number/test_num/code
        separated by |

        results[problem_number][test_number] = result
        results[problem_number] = [r0, r1, r2, ...etc] (None if no result)
        """
        test_results = test_results.decode("utf-8")
        if test_results is "":
            self.results[problem_number] = (
                [(3, "Failed to compile")] *
                (self.assignment.problems[problem_number].tests + 1))
        results = test_results.split("|")
        for r in results:
            sections = r.split("/")
            problem = sections[0]
            if problem not in self.results:
                self.results[problem] = (
                    [(3, "Failed to compile")] *
                    (self.assignment.problems[problem].tests + 1))
            self.results[problem][int(sections[1])] = (int(sections[3]),
                                                       sections[2])

    def run_sml(self, problem_number: Text):
        print(f"{self.name} sml: {problem_number}")
        self.start()
        try:
            self.server.run_file(self.problems[problem_number])
            self.parse_test_results(
                self.server.get_results(problem_number), problem_number)
        except KeyError:
            return
        except HTTPException:
            self.started = False

    """
    Defining other modes of grading

    Each function can run independently, but for grading purposes
    self.results should be updated in the format of
    self.results[problem_number][test_number] = return code

    see results_to_string() for a list of return codes
    """

    def run_a52(self, problem_number: Text):
        print(f"a52: {problem_number}")
        current_problem = self.assignment.problems[problem_number]
        expected_answer = int(current_problem.answer)
        filename = path.join(
            self.dir, f"{self.name}-{current_problem.filename}.a52")
        test = current_problem.test_path
        output = run_a52(filename, test, DEFAULT_PATH_TO_JAR)
        res = match("CS52 says > (-?\d+).*", output, DOTALL)
        if res is None:
            if output is not "":
                self.results[problem_number] = [(1, output.rstrip())]
            else:
                self.results[problem_number] = [(2, "Encountered other error - file not found?")]
        else:
            actual_answer = int(res.groups(0)[0])
            if actual_answer == expected_answer:
                self.results[problem_number] = [(0, "Correct")]
            else:
                self.results[problem_number] = [(
                    2,
                    f"Expected {expected_answer}, got {actual_answer}")]

    def run_a52_direct(self, problem_number: Text):
        current_problem = self.assignment.problems[problem_number]

        run_file = current_problem.runfile
        run_file = path.join(self.grading_path, run_file)
        input_file = path.join(self.dir,
                               f"{self.name}-{current_problem.input}")
        expected_answer = int(current_problem.answer)
        print(run_file, input_file)
        output = run_a52(run_file, input_file, DEFAULT_PATH_TO_JAR)
        res = match("CS52 says > (-?\d+).*", output, DOTALL)
        if res is None:
            self.results[problem_number] = [(1, output.rstrip())]
        else:
            actual_answer = int(res.groups(0)[0])
            if actual_answer == expected_answer:
                self.results[problem_number] = [(0, "Correct")]
            else:
                self.results[problem_number] = [(
                    2,
                    f"Expected {expected_answer}, got {actual_answer}")]

    def run_dfa(self, problem_number: Text):
        pass

    def run_tur(self, problem_number: Text):
        pass

    def run_problem(self, problem_number: Text):
        print(f"{self.name} run: {problem_number}")
        """Runs the file associated with the problem number
        If nothing is specified, runs the next problem
                after the last one previously run
        """
        print("run problem")
        problem_mode = self.assignment.problems[problem_number].mode
        {"sml": self.run_sml,
         "a52": self.run_a52,
         "a52_direct": self.run_a52_direct,
         "dfa": self.run_dfa,
         "tur": self.run_tur}.get(problem_mode)(problem_number)

    def run_all(self):
        """
        Runs all problems in the assignment
        """

        if any(v.mode is "sml" for k, v in self.assignment.problems.items()):
            self.start()
            if self.assignment.starter_file is not None:
                self.server.run_file(self.assignment.starter_file)

        for (p_name, p) in self.assignment.problems.items():
            try:
                self.run_problem(p_name)
            except socket.timeout:
                self.end()
        self.end()
