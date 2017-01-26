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