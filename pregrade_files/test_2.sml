fun test1 information help function arg1 arg2 retval =
  if function arg1 arg2 = retval
    then print(information ^ ":\t PASS\n")
  else
    print (information ^ ":\t FAIL\n\t" ^ help);
