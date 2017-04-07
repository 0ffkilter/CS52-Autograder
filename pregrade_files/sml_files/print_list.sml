fun printList nil     = ()
  | printList (s::ss) = (print (s ^ "\n"); printList ss);