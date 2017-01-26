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
