# programming-language

Currently just a tokenizer test. Run `lang.py` and give it a program as input, and it will tokenize it.

# syntax

`“string”`: string of arbitrary length. `\k` for any character `k` currently returns `k` for most `k`; changes will be made later.  
`“string1“string2“string3”`: list of strings of arbitrary length, of arbitrary length. String syntax still applies  
`”c`: string of length `1`. `'\k` still works, still giving `k` though.  
`123`: number  
`0123`: octal  
`0b11`: binary  
`0q11`: quaternary  
`0x11`: hexadecimal
`[1 2 3]`: list. Can be nested like `[1 2 3 [4 5 6]]`. Try `[1[2[3[4]5]6]7]` :D  

# codeblocks
`ßcode»`: sort over a key function. If top-of-stack is a list, sort that; otherwise, sort the whole stack  
`€code»`: map over a key function. If top-of-stack is a list, map that; otherwise, map the whole stack  
`þcode»`: filter over a key function. If top-of-stack is a list, filter that; otherwise, filter the whole stack  
`ʠcode»`: filter out over a key function. If top-of-stack is a list, filter out that; otherwise, apply on the whole stack  
`/code»`: reduce over a key (dyadic) function.

Codeblocks do not need the trailing '»'; that's only required for if `code` contains more than one token.  

# commands
`¬`: Logical inverse  
`×`: Multiply  
`ı`: Complex Number  
`ȷ`: `1-from-top * 10 ** top` (exp-10)  
`&`: Logical AND  
`+`: Addition (Integer, String)  
`-`: Negate (Integer)  
`?`: Ternary: `2-from-top if top else 1-from-top`
`B`: Integer -> Binary Digits, or String -> Characters; does nothing to multi-value things
`D`: Integer -> Decimal Digits, or String -> Characters; does nothing to multi-value things  
`J`: Range of Length (according to `L`)
`L`: Length; converts numbers to strings automatically  
`O`: String -> Map to code-points, Character -> code-point, Integer -> character at that code-point  
`R`: Range `[1..x]`  
`U`: Reverses the top if it can be iterated over; otherwise, the whole stack  
`_`: Subtraction; `1-from-top - top`
`|`: Logical OR  
`Ạ`: Python AND  
`Ḷ`: Range `[0..x-1]`  
`Ọ`: Python OR  
`Ḃ`: Binary digits -> Integer  
`Ḋ`: Decimal digits -> Integer  
`‘`: Increment  
`’`: Decrement  
