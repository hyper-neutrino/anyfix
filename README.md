# programming-language

Currently just a tokenizer test. Run `lang.py` and give it a program as input, and it will tokenize it.

# syntax

`“string”`: string of arbitrary length. `\k` for any character `k` currently returns `k` for most `k`; changes will be made later.  
`“string1“string2“string3”`: list of strings of arbitrary length, of arbitrary length. String syntax still applies  
`”c`: string of length `1`. `'\k` still works, still giving `k` though.  
`123`: number  
`0123`: octal  
`0b11`: binary  
`0k11`: base something: binary = b, ternary = t, quaternary = q, base 5 = p, base 6 = h, base 7 = s, base 9 = n, base 11 = U, base 12   = d, base 13 = T, base 14 = Q, base 15 = P, base 16 = x, base 17 = S, base 18 = O, base 19 = N, base 20 = M  
`[1 2 3]`: list. Can be nested like `[1 2 3 [4 5 6]]`. Try `[1[2[3[4]5]6]7]` :D  
