fun test_2_list information help function arg1 arg2 retval =
	if (list_compare (function arg1 arg2) (retval)) = true
		then print(information ^ ":\t PASS\n")
	else
		print (information ^ ":\t FAIL\n\t" ^ help ^ "\n");