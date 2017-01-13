fun test1 information help function arg1 retval =
	if function arg1 = retval
		then print(information ^ ":\t PASS\n")
	else
		print (information ^ ":\t FAIL\n\t" ^ help);
