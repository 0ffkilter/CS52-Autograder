fun test_1_list information help function arg1 arg2 =
	if (list_compare_exact (function arg1 arg2) (retval)) = true
		then print(information ^ ":\t PASS\n")
	else
		print (information ^ ":\t FAIL\n\t" ^ help);