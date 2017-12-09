## Autograding

### General Usage

```
usage: autograder.py [-h] [-c] [-d] [-s] [-g] [-p] [-t] [--student STUDENT]
                     [--submission-folder SUBMIT_FOLDER]
                     [--grading-folder GRADING_FOLDER] [--num-zips NUM_ZIPS]
                     [--num-threads NUM_THREADS]
                     assignment

Autograde an assignment

positional arguments:
  assignment

optional arguments:
  -h, --help            show this help message and exit
  -c                    Collect student files
  -d                    Delete the asgt0N-folder and make a new one
  -s                    Setup files for grading
  -g                    Grade files that are gathered
  -p                    Package files for distribution
  -t                    Generate fake assignment before grading
  --student STUDENT     Only grade a certain student's files
  --submission-folder SUBMIT_FOLDER
                        Point to the submission folder - defaults to
                        asgt0N-submissions
  --grading-folder GRADING_FOLDER
                        Point to the output folder - defaults to asgt0N-ready
  --num-zips NUM_ZIPS   Number of zips to package into - default 3
  --num-threads NUM_THREADS
                        Number of threads to use for concurrency - default 4
```

If you want to do everything start to finish for assignment N, use

```
python3 autograder.py -c -s -g -p N
```

A bit more about the other arguments

* the ```-d``` flag will delete ```asgt0N-ready``` in case you want to redo everything
* the ```-t``` flag will create a fake submission for unit testing, see that section for more details

```--submission-folder folder``` will change the default folder from ```asgt0N-submissions``` to folder

```--grading-folder folder``` will change the default output folder from ```asgt0N-ready``` to folder

```--num-zips X``` will change the number of zip packages from 3 to X when distributing

```--num-threads Y``` will change the number of threads used for grading from 4 to Y  


### Gathering Files

```-c``` for Collect

Gathering files implies copying over the files specified in the ```Files``` section of the assignment config to the student's folder in the output folder (default ```asgt0N-ready```).  Additionally, the file will be renamed to ```NAME-filename.txt``` where NAME is the student's name and filename is the original filename.

Additionally, a .timestamps.txt file is created in the students folder containing the last known submission for each of the files submitted.  

### Setting up Grading Files

```-s``` for Setup (look, they all started with g)

This does a couple of things, dependent on the types of problems the assignment contains.

All of these things are in the ```asgt0N-ready/student-name``` folder.  Some things are general and occur once per assignment if any problem is of this type, and some are on a per problem basis

#### SML

###### General Setup
If any problem is SML, a ```grading/``` folder is created in the student's folder and the ```assert.sml``` file is copied over to make sure the tests can be run outside of the autograder program

###### Problem Setup
For a generic SML problem, in ```grading/``` each problem will have an sml file created, named ```asgt0A_B.sml``` where ```A``` is the assignment number and ```B``` is the problem number.  

#### A52 (CS52-Machine)

###### General Setup

3 Library Files (```mullib.a52, divilib.a52, divrlib.a52```) are copied to the student's directory, as well as a script to run the tests given.  Additionally, a copy of the cs52 machine jar is distributed to each of the student directories.

A ```grading/``` folder is also created to copy the tests into.

###### Problem Setup

Each of the test files (list of integers) is copied into the ```grading/``` directory. 

#### A52-Direct

A52-Direct is the name given to a problem that has a student submit a list of integers as input for a given file.  In this, the professor has given them a file and the students must come up with input to make the file output the correct answer.  

##### General Setup

Follows the same rules as ```A52```

##### Problem Setup 

The given file is copied to the ```grading/``` directory while the student's input remains in the general directory as a collected file.  

#### SML_A52

Same as SML General.  Note that unlike A52, no copy of the cs52 jar is provided.

#### Visual

No setup

#### JFlap

##### General Setup

Nothing specific

##### Problem Setup

Each test is provided to the grader in the ```grading/``` folder


### Grading

The general grading formula is as follows:

For a problem worth ```N``` points with ```T``` tests

```
The student starts with N points.

For each failed test, the student loses 0.5 points.

However, the student will receive a 0 on the problem if and only if T tests (all of them) are failed.
(In this situation, it falls to a human grader to assign partial credit, if applicable)
```

Grades are put into ```asgt0N-grades.txt``` with the results of each test and a summary of how the assignment was scored.  

### Packaging

For distribution to the graders, the assignments are packed into zips organized alphabetically by name.  In the event of overflow or uneven distributions, the extras are given to the earlier groups.

Example:
```
For a distribution of 11 assignments (1-11) and a split of 3, they would be named
1-4.zip (1,2,3,4)
5-8.zip (5,6,7,8)
9-11.zip (9,10,11)

```

### Emailing

See Email.md

### Unit Testing

See Unit-Test.md