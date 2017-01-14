fun test_3_exact information help function arg1 arg2 arg3 retval =
	if (list_compare_exact (function arg1 arg2 arg3) (retval)) = true
		then print(information ^ ":\t PASS\n")
	else
		print (information ^ ":\t FAIL\n\t" ^ help);