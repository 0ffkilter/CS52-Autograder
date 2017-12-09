## Basic Unit Testing

The Autograder has a (very basic) unit test feature that will generate a mock assignment before running the autograder. 

The ```-t``` flag (for Test) will make the assignment, and copy files into each student's directory.

The default path to look is in ```CS52-GradingScripts/assignments/asgt0N/resources/``` where the files should live.  

Let's consider a sample assignment - assignment 5:

Assume the assignment grading config is located in ```CS52-GradingScripts/assignments/asgt0N/```

If in ```asgt05/config.ini``` the ```Assignment```Section reads as such:


```
[Assignment]
TotalPoints = 23
StylePoints = 2
NumProblems = 5
Mode = a52
Files = nonuple.a52,power2.a52,oddfact.a52,ackermann.a52,asgt04-5.txt
DueDate = 2017-02-024 17:00:00
```

The unit tester would expect the following file structure:

```
| - CS52-GradingScripts/
	| - assignments/
		| - asgt05/
			| - resources/
				| - nonuple.a52
				| - power2.a52
				| - oddfact.a52
				| - ackerman.a52
				| - asgt04-5.txt
			| - config.ini
			| - <tests>
		| - ... 
	| - data/
	| - scripts/
	| - ...
```

A sample asgt05-submissions folder will be created, given the correct name, and each file will be copied over.

The intention is for the solutions to be located in the resources/ folder, so you know if all of your tests pass.  