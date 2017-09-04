import http.client
import subprocess
from os import path
from typing import Optional, Text, List


DEFAULT_SERVER_LOCATION = path.abspath("C:/Users/Matt/Dev/CS52-Autograder/serve-sml")

DEFAULT_PORT = 8181
DEFAULT_FILE_ORDER = [path.join(DEFAULT_SERVER_LOCATION, f'{p}.sml').replace("\\", "/")
                 for p in ["buffer", "util", "http", "server", "assert", "grading_lib", "main"]]

class ServerHandler:

    def __init__(self, port: Optional[int] = None, server_location: Optional[str] = None):
        """Make the Server object

        Args:
        Server_location:  Where the sml files are located
        files:  the files (and order) that they should be run in
        """
        self.server_location = server_location or DEFAULT_SERVER_LOCATION
        self.sml_string = " ".join([f'use \"{f}\";' for f in DEFAULT_FILE_ORDER])
        self.port = port or DFEAULT_PORT
        self.sml_string = f"val default_port = {self.port}; {self.sml_string}"
        self.process = None
        self.has_started = False

    def get_response(self, get_string: Text) -> http.client.HTTPResponse:
        """Get the response from a GET request

        The server only supports GET, so that's why it's hardcoded
        """

        conn = http.client.HTTPConnection(f"localhost:{self.port}")
        conn.request("GET", get_string)
        return conn.getresponse()

    def get_process(self) -> subprocess.Popen:
        """ Starts the process (if not already running), or returns the current
        """

        if self.has_started:
            return self.process

        self.process = subprocess.Popen(f"echo {self.sml_string} | sml", shell=True)
        self.has_started = True
        return self.process

    def check_response(self, resp: http.client.HTTPResponse) -> bool:
        """Returns True if the response is 200 status and has 'Ok'"""
        return resp.status == 200

    def check_status(self) -> bool:
        """Returns True if the server is up, False otherwise"""

        resp = self.get_response("status")
        return self.check_response(resp)

    def run_file(self, filename: Text) -> bool:
        """Run a file on the server

        Args:
        filename:  Complete path to run
        """

        resp = self.get_response("file/" + filename)
        return self.check_response(resp)

    def get_results(self, problem_number: Text, sub_problem_number: Text = None):
        """Get the results of tests back from the server
        
        Args:
        problem_number:  The number of the problem.  Convert to string beforehand ("1" not 1)
        sub_problem_number:  The letter (or number) of the subproblem.  Should also be string
        """

        resp = None
        if sub_problem_number is None:
            resp = self.get_response(f"results/{problem_number}")
        else:
            resp = self.get_response(f"results/{problem_number}/{sub_problem_number}")
        if self.check_response(resp):
            return resp.read()
        return None

    def kill(self) -> bool:
        """Kills the server.  Returns true if server is dead, false otherwise
        """
        try:
            #Should Error if server is properly dead
            self.get_response("kill")
            return False
        except ConnectionResetError:
            self.has_started = False
            return True
        except http.client.ResponseNotReady:
            return False
        return False

    def start(self) -> bool:
        """Starts the server.  Returns true if server is up, false otherwise
        """
        try:
            self.get_process()
        except ConnectionRefusedError:
            self.has_started = False
            return False
        print("hello?")
        return self.check_status()
