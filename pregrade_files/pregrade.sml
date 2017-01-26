(*** list_compare.sml $+list_compare.sml ***)
fun list_compare [] [] = true
  | list_compare [] _ = false
  | list_compare (x::xs) [] = false
  | list_compare (x::xs) (y) = 
        let 
            fun delete _     [] = []
              | delete value (x::xs) = if x = value
                                then xs
                            else x::(delete value xs);
            val lst = delete x y
        in
            list_compare xs lst
        end;

(*** list_compare.sml $-list_compare.sml ***)

(*** list_compare_exact.sml $+list_compare_exact.sml ***)
fun list_compare_exact [] [] = true
  | list_compare_exact [] _  = false
  | list_compare_exact _  [] = false
  | list_compare_exact (x::xs) (y::ys) = (x = y) andalso (list_compare_exact xs ys);

(*** list_compare_exact.sml $-list_compare_exact.sml ***)

(*** test_1.sml $+test_1.sml ***)
fun test_1 information help function arg1 retval =
	if function arg1 = retval
		then print(information ^ ":\t PASS\n")
	else
		print (information ^ ":\t FAIL\n\t" ^ help ^ "\n");

(*** test_1.sml $-test_1.sml ***)

(*** test_1_error.sml $+test_1_error.sml ***)
fun test_1_error information help function arg1 error =
	let 
		fun error_help func arg err = 
			let 
				val res = func arg <> func arg
					handle err => true
			in
				res
		end
	in
		if error_help function arg1 error = true
			then print (information ^ ":\t PASS\n" )
		else
			print (information ^ ":\t FAIL\n\t" ^ help ^ "\n")
	end;
(*** test_1_error.sml $-test_1_error.sml ***)

(*** test_1_exact.sml $+test_1_exact.sml ***)
fun test_1_exact information help function arg1 retval =
	if list_compare_exact (function arg1) (retval) = true
		then print(information ^ ":\t PASS\n")
	else
		print (information ^ ":\t FAIL\n\t" ^ help ^ "\n");
(*** test_1_exact.sml $-test_1_exact.sml ***)

(*** test_1_list.sml $+test_1_list.sml ***)
fun test_1_list information help function arg1 =
	if list_compare (function arg1) (retval) = true
		then print(information ^ ":\t PASS\n")
	else
		print (information ^ ":\t FAIL\n\t" ^ help ^ "\n");
(*** test_1_list.sml $-test_1_list.sml ***)

(*** test_1_real.sml $+test_1_real.sml ***)
fun test_1_real information help function arg1 retval =
	if Real.==((function arg1), retval) = true
		then print(information ^ ":\t PASS\n")
	else
		print (information ^ ":\t FAIL\n\t" ^ help ^ "\n");

(*** test_1_real.sml $-test_1_real.sml ***)

(*** test_2.sml $+test_2.sml ***)
fun test_2 information help function arg1 arg2 retval =
  if function arg1 arg2 = retval
    then print(information ^ ":\t PASS\n")
  else
    print (information ^ ":\t FAIL\n\t" ^ help ^ "\n");

(*** test_2.sml $-test_2.sml ***)

(*** test_2_error.sml $+test_2_error.sml ***)
fun test_2_error information help function arg1 arg2 error =
	let 
		fun error_help func arg arg_2 err = 
			let 
				val res = func arg arg_2 <> func arg arg_2
					handle err => true
			in
				res
		end
	in
		if error_help function arg1 arg2 error = true
			then print (information ^ ":\t PASS\n" )
		else
			print (information ^ ":\t FAIL\n\t" ^ help ^ "\n")
	end;
(*** test_2_error.sml $-test_2_error.sml ***)

(*** test_2_exact.sml $+test_2_exact.sml ***)
fun test_2_exact information help function arg1 arg2 retval =
	if (list_compare_exact (function arg1 arg2) (retval)) = true
		then print(information ^ ":\t PASS\n")
	else
		print (information ^ ":\t FAIL\n\t" ^ help ^ "\n");
(*** test_2_exact.sml $-test_2_exact.sml ***)

(*** test_2_list.sml $+test_2_list.sml ***)
fun test_2_list information help function arg1 arg2 retval =
	if (list_compare (function arg1 arg2) (retval)) = true
		then print(information ^ ":\t PASS\n")
	else
		print (information ^ ":\t FAIL\n\t" ^ help ^ "\n");
(*** test_2_list.sml $-test_2_list.sml ***)

(*** test_3.sml $+test_3.sml ***)
fun test_3 information help function arg1 arg2 arg3 retval =
  if function arg1 arg2 arg3 = retval
    then print(information ^ ":\t PASS\n")
  else
    print (information ^ ":\t FAIL\n\t" ^ help ^ "\n");

(*** test_3.sml $-test_3.sml ***)

(*** test_3_error.sml $+test_3_error.sml ***)
fun test_3_error information help function arg1 arg2 arg3 error =
	let 
		fun error_help func arg arg_2 arg_3 err = 
			let 
				val res = func arg arg_2 arg_3 <> func arg arg_2 arg_3
					handle err => true
			in
				res
		end
	in
		if error_help function arg1 arg2 arg3 error = true
			then print (information ^ ":\t PASS\n" )
		else
			print (information ^ ":\t FAIL\n\t" ^ help ^ "\n")
	end;
(*** test_3_error.sml $-test_3_error.sml ***)

(*** test_3_exact.sml $+test_3_exact.sml ***)
fun test_3_exact information help function arg1 arg2 arg3 retval =
	if (list_compare_exact (function arg1 arg2 arg3) (retval)) = true
		then print(information ^ ":\t PASS\n")
	else
		print (information ^ ":\t FAIL\n\t" ^ help ^ "\n");
(*** test_3_exact.sml $-test_3_exact.sml ***)

(*** test_3_list.sml $+test_3_list.sml ***)
fun test_3_list information help function arg1 arg2 arg3 retval =
	if (list_compare (function arg1 arg2 arg3) (retval)) = true
		then print(information ^ ":\t PASS\n")
	else
		print (information ^ ":\t FAIL\n\t" ^ help ^ "\n");
(*** test_3_list.sml $-test_3_list.sml ***)

(*** value_compare.sml $+value_compare.sml ***)
fun value_compare information help value expected =
	if value = expected
		then print(information ^ ":\t PASS\n")
	else
		print (information ^ ":\t FAIL\n\t" ^ help ^ "\n");

(*** value_compare.sml $-value_compare.sml ***)

