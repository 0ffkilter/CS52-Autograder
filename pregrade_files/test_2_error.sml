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