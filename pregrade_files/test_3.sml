fun test_3 information help function arg1 arg2 arg3 retval =
  if function arg1 arg2 arg3 = retval
    then print(information ^ ":\t PASS\n")
  else
    print (information ^ ":\t FAIL\n\t" ^ help);
