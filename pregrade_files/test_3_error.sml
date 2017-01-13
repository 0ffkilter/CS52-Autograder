fun test1_error information help function arg1 arg2 error =
	let 
		fun error_help func arg arg_2 arg_3 err = 
			let 
				val res = func arg arg_2 arg_3 <> func arg arg_2 arg_3
					handle err => true
			in
				res
		end
	in
		if error_help function arg1 arg2 arg_3 error = true
			then print (information ^ ":\t PASS\n" )
		else
			print (information ^ ":\t FAIL\n\t" ^ help)
	end;