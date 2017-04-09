(*** test_1_error_lex $+test_1_error_lex ***)
fun test_1_error_lex information help function arg1 = let fun error_help func arg = let val res = func arg <> func arg handle LexicalException msg => (print ("Printed Error: " ^ msg ^ "\n"); true) in res end in if error_help function arg1 = true then print (information ^ ":\t PASS\n" ) else print (information ^ ":\t FAIL\n\t" ^ help ^ "\n") end;
(*** test_1_error_lex $-test_1_error_lex ***)

(*** test_1_error_code $+test_1_error_code ***)
fun test_1_error_grammar information help function arg1 = let fun error_help func arg = let val res = func arg <> func arg handle CodeException msg => (print ("Printed Error: " ^ msg ^ "\n"); true) in res end in if error_help function arg1 = true then print (information ^ ":\t PASS\n" ) else print (information ^ ":\t FAIL\n\t" ^ help ^ "\n") end;
(*** test_1_error_code $-test_1_error_code ***)

(*** test_2 $+test_2 ***)
fun test_2 information help function arg1 arg2 retval = if function arg1 arg2 = retval then print(information ^ ":\t PASS\n") else print (information ^ ":\t FAIL\n\t" ^ help ^ "\n");
(*** test_2 $-test_2 ***)

(*** test_2_list $+test_2_list ***)
fun test_2_list information help function arg1 arg2 retval = if (list_compare (function arg1 arg2) (retval)) = true then print(information ^ ":\t PASS\n") else print (information ^ ":\t FAIL\n\t" ^ help ^ "\n");
(*** test_2_list $-test_2_list ***)

(*** test_2_error $+test_2_error ***)
fun test_2_error information help function arg1 arg2 error = let fun error_help func arg arg_2 err = let val res = func arg arg_2 <> func arg arg_2 handle err => true in res end in if error_help function arg1 arg2 error = true then print (information ^ ":\t PASS\n" ) else print (information ^ ":\t FAIL\n\t" ^ help ^ "\n") end;
(*** test_2_error $-test_2_error ***)

(*** test_3 $+test_3 ***)
fun test_3 information help function arg1 arg2 arg3 retval = if function arg1 arg2 arg3 = retval then print(information ^ ":\t PASS\n") else print (information ^ ":\t FAIL\n\t" ^ help ^ "\n");
(*** test_3 $-test_3 ***)

(*** list_compare_exact $+list_compare_exact ***)
fun list_compare_exact [] [] = true | list_compare_exact [] _ = false | list_compare_exact _ [] = false | list_compare_exact (x::xs) (y::ys) = (x = y) andalso (list_compare_exact xs ys);
(*** list_compare_exact $-list_compare_exact ***)

(*** print_list $+print_list ***)
fun printList nil = () | printList (s::ss) = (print (s ^ "\n"); printList ss);
(*** print_list $-print_list ***)

(*** test_1_exact $+test_1_exact ***)
fun test_1_exact information help function arg1 retval = if list_compare_exact (function arg1) (retval) = true then print(information ^ ":\t PASS\n") else print (information ^ ":\t FAIL\n\t" ^ help ^ "\n");
(*** test_1_exact $-test_1_exact ***)

(*** test_1_error $+test_1_error ***)
fun test_1_error information help function arg1 error = let fun error_help func arg err = let val res = func arg <> func arg handle err => true in res end in if error_help function arg1 error = true then print (information ^ ":\t PASS\n" ) else print (information ^ ":\t FAIL\n\t" ^ help ^ "\n") end;
(*** test_1_error $-test_1_error ***)

(*** test_1 $+test_1 ***)
fun test_1 information help function arg1 retval = if function arg1 = retval then print(information ^ ":\t PASS\n") else print (information ^ ":\t FAIL\n\t" ^ help ^ "\n");
(*** test_1 $-test_1 ***)

(*** test_1_list $+test_1_list ***)
fun test_1_list information help function arg1 retval= if list_compare (function arg1) (retval) = true then print(information ^ ":\t PASS\n") else print (information ^ ":\t FAIL\n\t" ^ help ^ "\n");
(*** test_1_list $-test_1_list ***)

(*** test_1_error_grammar $+test_1_error_grammar ***)
fun test_1_error_grammar information help function arg1 = let fun error_help func arg = let val res = func arg <> func arg handle GrammarException msg => (print ("Printed Error: " ^ msg ^ "\n"); true) in res end in if error_help function arg1 = true then print (information ^ ":\t PASS\n" ) else print (information ^ ":\t FAIL\n\t" ^ help ^ "\n") end;
(*** test_1_error_grammar $-test_1_error_grammar ***)

(*** test_1_real $+test_1_real ***)
fun test_1_real information help function arg1 retval = if Real.==((function arg1), retval) = true then print(information ^ ":\t PASS\n") else print (information ^ ":\t FAIL\n\t" ^ help ^ "\n");
(*** test_1_real $-test_1_real ***)

(*** test_3_error $+test_3_error ***)
fun test_3_error information help function arg1 arg2 arg3 error = let fun error_help func arg arg_2 arg_3 err = let val res = func arg arg_2 arg_3 <> func arg arg_2 arg_3 handle err => true in res end in if error_help function arg1 arg2 arg3 error = true then print (information ^ ":\t PASS\n" ) else print (information ^ ":\t FAIL\n\t" ^ help ^ "\n") end;
(*** test_3_error $-test_3_error ***)

(*** test_3_list $+test_3_list ***)
fun test_3_list information help function arg1 arg2 arg3 retval = if (list_compare (function arg1 arg2 arg3) (retval)) = true then print(information ^ ":\t PASS\n") else print (information ^ ":\t FAIL\n\t" ^ help ^ "\n");
(*** test_3_list $-test_3_list ***)

(*** test_3_exact $+test_3_exact ***)
fun test_3_exact information help function arg1 arg2 arg3 retval = if (list_compare_exact (function arg1 arg2 arg3) (retval)) = true then print(information ^ ":\t PASS\n") else print (information ^ ":\t FAIL\n\t" ^ help ^ "\n");
(*** test_3_exact $-test_3_exact ***)

(*** value_compare $+value_compare ***)
fun value_compare information help value expected = if value = expected then print(information ^ ":\t PASS\n") else print (information ^ ":\t FAIL\n\t" ^ help ^ "\n");
(*** value_compare $-value_compare ***)

(*** test_2_knuth $+test_2_knuth ***)
fun test_2_knuth information help function arg1 arg2 retval = let val result = function arg1 arg2 val permutation = list_compare result retval val isSame = list_compare_exact result retval in if permutation = true andalso isSame = false then print(information ^ ":\t PASS\n") else print (information ^ ":\t FAIL\n\t" ^ help ^ "\n") end;
(*** test_2_knuth $-test_2_knuth ***)

(*** test_2_exact $+test_2_exact ***)
fun test_2_exact information help function arg1 arg2 retval = if (list_compare_exact (function arg1 arg2) (retval)) = true then print(information ^ ":\t PASS\n") else print (information ^ ":\t FAIL\n\t" ^ help ^ "\n");
(*** test_2_exact $-test_2_exact ***)

(*** list_compare $+list_compare ***)
fun list_compare [] [] = true | list_compare [] _ = false | list_compare (x::xs) [] = false | list_compare (x::xs) (y) = let fun delete _ [] = [] | delete value (x::xs) = if x = value then xs else x::(delete value xs); val lst = delete x y in list_compare xs lst end;
(*** list_compare $-list_compare ***)

