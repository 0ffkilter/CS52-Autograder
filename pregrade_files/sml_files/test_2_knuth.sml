fun test_2_knuth information help function arg1 arg2 retval =
    let 
        val result = function arg1 arg2
        val permutation = list_compare result retval
        val isSame = list_compare_exact result retval
    in 
        if permutation = true andalso isSame = false
            then print(information ^ ":\t PASS\n")
        else
            print (information ^ ":\t FAIL\n\t" ^ help ^ "\n")
    end;
