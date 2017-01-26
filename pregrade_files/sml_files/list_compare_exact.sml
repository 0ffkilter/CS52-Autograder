fun list_compare_exact [] [] = true
  | list_compare_exact [] _  = false
  | list_compare_exact _  [] = false
  | list_compare_exact (x::xs) (y::ys) = (x = y) andalso (list_compare_exact xs ys);
