import http.client
import subprocess
import os

DEFAULT_SERVER_LOCATION = "C:/Users/Matt/Dev/CS52-Autograder/serve-sml"
DEFAULT_FILE_ORDER = ["buffer", "util", "http", "server", "assert", "grading_lib", "main"]

class ServerHandler:

    def __init__(self, server_location:str=None, files:list=None):
        """Make the Server object

        Args:
        Server_location:  Where the sml files are located
        files:  the files (and order) that they should be run in
        """

        if server_location is not None:
            self.server_location = server_location
        else:
            self.server_location = DEFAULT_SERVER_LOCATION

        if files is not None:
            self.files = files
        else:
            self.files = DEFAULT_SERVER_LOCATION

        self.process = None
        self.has_started = False

    def get_response(self, get_string:str) -> http.client.HTTPResponse:
        """Get the response from a GET request

        The server only supports GET, so that's why it's hardcoded
        """

        conn = http.client.HTTPConnection("localhost:8181")
        conn.request("GET", get_string)
        return conn.getresponse()

    def get_process(self) -> subprocess.Popen:
        """ Starts the process (if not already running), or returns the current
        """

        if not self.has_started:
            sml_string = " ".join(["use \"%s.sml\";" %(self.server_location + "/" + f) for f in self.files])
            self.process = subprocess.Popen("echo %s | sml" %(sml_string), shell=True)
            self.has_started = True
            return self.process
        else:
            return self.process

    def check_response(self, resp:http.client.HTTPResponse) -> bool:
        """Returns True if the response is 200 status and has 'Ok'"""

        return resp.status == 200 and resp.reason == "Ok"

    def check_status(self) -> bool:
        """Returns True if the server is up, False otherwise"""

        resp = self.get_response("status")
        return self.check_response(resp)

    def run_file(self, filename:str) -> bool:
        """Run a file on the server

        Args:
        filename:  Complete path to run
        """

        resp = self.get_response("file/" + filename)
        return self.check_response(resp)

    def get_results(self, problem_number:str, sub_problem_number:str=None):
        """Get the results of tests back from the server
        
        Args:
        problem_number:  The number of the problem.  Convert to string beforehand ("1" not 1)
        sub_problem_number:  The letter (or number) of the subproblem.  Should also be string
        """

        resp = None
        if sub_problem_number == None:
            resp = self.get_response("results/%s" %(problem_number))
        else:
            resp = self.get_response("results/%s/%s" %(problem_number, sub_problem_number))
        if self.check_response(resp):
            return resp.read()
        else:
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
        return self.check_status()

if __name__ == '__main__':
    """Sample testing"""
    server = ServerHandler()
    print(server.start())
    print(server.run_file("C:/Users/Matt/Dev/CS52-Autograder/serve-sml/example_sml/sample_assignment.sml"))
    print(server.run_file("C:/Users/Matt/Dev/CS52-Autograder/serve-sml/example_sml/simple_test.sml"))
    print(server.run_file("C:/Users/Matt/Dev/CS52-Autograder/serve-sml/example_sml/simple_test_2.sml"))
    print(server.get_results("1"))
    print(server.kill())
