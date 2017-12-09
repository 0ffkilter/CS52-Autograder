## Installation

### Requires Python 3.6

1. Clone the repo

```
git clone https://github.com/0ffkilter/CS52-Autograder.git
```

2. Install the submodules

```
git submodule init
git submodule update
```

Note: You may need to ask for permission to clone the CS52-GradingScripts repo as it contains sensitive information

3. Install pip dependencies

```
$ pip3 install -r requirements.txt
```

Note: may just be pip

4. Link CS52-Autograder/grading_scripts to CS52-Autograder/CS52-GradingScripts

Windows:
```
> mklink /d /path/to/CS52-Autograder/grading_scripts /path/to/CS52-Autograder/CS52-GradingScripts
```

Unix:
```
$ ln -s /path/to/CS52-Autograder/CS52-GradingScripts /path/to/CS52-Autograder/grading_scripts
```
