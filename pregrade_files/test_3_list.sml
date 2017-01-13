fun test_1_list information help function arg1 arg2 arg3 =
	if (list_compare (function arg1 arg2 arg3) (retval)) = true
		then print(information ^ ":\t PASS\n")
	else
		print (information ^ ":\t FAIL\n\t" ^ help);