# CS52-Autograder:

Autograder for CS052, Fundamentals of Computer Science

Written in Python 3.6 by Matthew Gee and Everett Bull

## Installation:

1.  Initialize the Grading Scripts sub repo

~~~
git submodule init
~~~

2.  Clone the Repo

~~~
git submodule update
~~~

3.  Link ./CS52-GradingScripts to ./grading_scripts/
~~~
ln -s /path/to/Autograder/CS52-GradingScripts /path/to/Autograder/grading_scripts
~~~

4.  (Optional) Install pip requirements to generate student list from Sakai Rosters
~~~
pip install -r CS52-GradingScripts/requirements.txt
~~~

## Usage:

#### Grading:

Gathers files and grades the entire assignment

```Bash
python autograder.py --grade <assign_num> 
```
Gathers files and grades any student with a regex match on <student_name> in either their name or email
```
python autograder.py --grade <assign_num> --student <student_name>
```

### Gather Files:

Gathers all files and generates SML subfiles but does not grade
```
python autograder.py --gather <assign_num>
```

Gathers files and grades any student with a regex match on <student_name> in either their name or email
```
python autograder.py --gather <assign_num> --student <student_name>
```

### Check

Checks the files of each student for the assignment
```
python autograder.py --check <assign_num>
```
Checks the files of a particular student
| The student name must match exactly the name in asgt0N-ready/
```
python autograder.py --check <assign_num> --student <student_name>
```

### Print

Prints the files of the assignment (but not the subfiles)
```
python autograder.py --print <assign_num>
```
Prints one student's files
| The student name must match exactly the name in asgt0N-ready/
```
python autograder.py --print <assign_num> --student <student_name>
```

### [Flag] Overwrite 

When used, any files copied or created will forcibly overwrite the files in the directory, eliminating any changes made to the asgt-ready/ folder

```
--overwrite
```

## Additional Tools

### Generate Assignment

```
python generate_assignment.py <assign_num> file1 file2 file3...
```
Generates a fake assignment in ```asgt0<assign_num>-submissions```, copying each ```file1 file2...``` into each students directory.

* Does not rename files


### pregrade_files/Generate Pregrade

```
python generate_pregrade.py
```

Generates a pregrade.sml containing all flags and code from the files.  Set ```compact=False``` in the file to preserve original spacing and tabs. 


### Checkout Files
```
python checkout_files.py <assign_num> <start_student> <end_student>
```

Zips the students from start->end (inclusive on both ends) into a zip in the current directory











