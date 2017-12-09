from os.path import join, abspath
from os import getcwd

DEFAULT_GRADING_PATH = join("grading_scripts", "assignments")

REZIP_CODE = """
import zipfile
import os
FIRST="%s"
LAST="%s"
ASSIGN_NUM=%i
def zipdir(path, zipf):
    for root, dirs, files in os.walk(path):
        for f in files:
            zipf.write(os.path.join(root, f))
zipf = zipfile.ZipFile("asgt0" + str(ASSIGN_NUM) + "-finished-" + FIRST + "-" + LAST + ".zip", 'w', zipfile.ZIP_DEFLATED)
zipdir('asgt0' + str(ASSIGN_NUM) + '-ready', zipf)
zipf.close()
"""

RUN_A52 = """
from subprocess import Popen
from sys import argv
from os.path import join
name = "$NAME$"
problem = argv[1]
file = "%s-%s.a52" %(name, problem)
test = argv[2]
test_file = join("grading", "%s_%s" %(problem, test))
cmd = "java -jar cs52-machine.jar -p %s -u %s" %(file, test_file)
with Popen(cmd, shell=True) as p:
    pass
"""

DEFAULT_SERVER_LOCATION = abspath(join(getcwd(), "serve-sml"))

DEFAULT_PORT = 8181

DEFAULT_FILE_ORDER = [join(DEFAULT_SERVER_LOCATION,
                                f'{p}.sml').replace("\\", "/")
                                for p in ["buffer", "util", "http",
                                          "server", "assert",
                                          "grading_lib", "main"]]

DEFAULT_PATH_TO_ASSERT = join("serve-sml", "assert.sml")
DEFAULT_PATH_TO_A52_LIBS = join("grading_scripts", "data")
DEFAULT_A52_LIBRARY_FILES = ["divilib.a52", "divrlib.a52", "mullib.a52"]
DEFAULT_PATH_TO_JAR = join("grading_scripts", "data", "cs52-machine.jar")
