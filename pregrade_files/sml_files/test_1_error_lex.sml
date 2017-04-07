fun test_1_error_lex information help function arg1 =
    let 
        fun error_help func arg = 
            let 
                val res = func arg <> func arg
                    handle LexicalException msg => (print ("Printed Error: " ^ msg ^ "\n"); true)
            in
                res
        end
    in
        if error_help function arg1 = true
            then print (information ^ ":\t PASS\n" )
        else
            print (information ^ ":\t FAIL\n\t" ^ help ^ "\n")
    end;
