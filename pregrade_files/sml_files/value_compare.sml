fun value_compare information help value expected =
	if value = expected
		then print(information ^ ":\t PASS\n")
	else
		print (information ^ ":\t FAIL\n\t" ^ help ^ "\n");
