fun list_compare [] [] = true
  | list_compare [] _  = false
  | list_compare _  [] = false
  | list_compare (x::xs) (y::ys) = (x = y) andalso (list_compare xs ys);
