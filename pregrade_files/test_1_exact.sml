fun test_1_exact information help function arg1
	if list_compare_exact (function arg1) (retval) = true
		then print(information ^ ":\t PASS\n")
	else
		print (information ^ ":\t FAIL\n\t" ^ help);