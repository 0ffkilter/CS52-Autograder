fun test1 information help function arg1 retval =
	if Real.==((function arg1), retval) = true
		then print(information ^ ":\t PASS\n")
	else
		print (information ^ ":\t FAIL\n\t" ^ help);
