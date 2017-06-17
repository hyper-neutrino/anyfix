# anyfix

## syntax

`“string”`: string of arbitrary length. `\k` for any character `k` currently returns `k` for most `k`; changes will be made later.  
`“string1“string2“string3”`: list of strings of arbitrary length, of arbitrary length. String syntax still applies  
`”c`: string of length `1`. `'\k` still works, still giving `k` though.  
`123`: number  
`0123`: octal  
`0b11`: binary  
`0q11`: quaternary  
`0x11`: hexadecimal
`[1 2 3]`: list. Can be nested like `[1 2 3 [4 5 6]]`. Try `[1[2[3[4]5]6]7]` :D  
`{1 2 3}`: set
`<1 2 3>`: tuple
`(1 2 3)`: splat (that is, all elements returned by its evaluation will be pushed independently onto the stack). Useful for overriding order of operations

## codeblocks
`ßcode»`: sort over a key function. If top-of-stack is a list, sort that; otherwise, sort the whole stack  
`€code»`: map over a key function. If top-of-stack is a list, map that; otherwise, map the whole stack  
`þcode»`: filter over a key function. If top-of-stack is a list, filter that; otherwise, filter the whole stack  
`ʠcode»`: filter out over a key function. If top-of-stack is a list, filter out that; otherwise, apply on the whole stack  
`/code»`: reduce over a key (dyadic) function.
`¿code»`: while loop; pop the top of the stack each time and if stack is non-empty and the popped value is true, run the code on the stack  

Codeblocks do not need the trailing '»'; that's only required for if `code` contains more than one token.  

## commands
`©`: Copy top of stack to register  
`¬`: Logical inverse  
`®`: Push register  
`×`: Multiply  
`ı`: Complex Number  
`ȷ`: `1-from-top * 10 ** top` (exp-10)  
`÷`: Float Division  
`!`: Factorial / Pi Function  
`"`: Duplicate top of stack  
`&`: Logical AND  
`+`: Addition (Integer, String)  
`-`: Negate (Integer)  
`:`: Integer Division  
`=`: Equality Check  
`?`: Ternary: `2-from-top if top else 1-from-top`  
`A`: Absolute Value  
`B`: Integer -> Binary Digits, or String -> Characters; does nothing to multi-value things
`D`: Integer -> Decimal Digits, or String -> Characters; does nothing to multi-value things  
`J`: Range of Length (according to `L`)
`L`: Length; converts numbers to strings automatically  
`O`: String -> Map to code-points, Character -> code-point, Integer -> character at that code-point  
`R`: Range `[1..x]`  
`S`: Sum  
`U`: Reverses the top if it can be iterated over; otherwise, the whole stack  
`_`: Subtraction; `1-from-top - top`  
`x`: Repeat List Element-wise (`[1 2 3] x 4` becomes `[1 1 1 1 2 2 2 2 3 3 3 3]`)  
`|`: Logical OR  
`¹`: Identity (returns the argument)  
`²`: Squared  
`³`: 16  
`⁴`: 10  
`⁵`: 100  
`⁶`: 1000  
`⁷`: ''  
`⁸`: '\n'  
`⁹`: []  
`⁺`: Only keep positive numbers and strings  
`¯`: Only keep negative numbers  
`⁼`: Check type equality  
`Ɠ`: Evaluate a single line of input  
`Ƥ`: Print followed by a newline  
`ƈ`: Read a single character of input  
`ɠ`: Read a line of input  
`ƥ`: Print not followed by a newline  
`Ạ`: Python AND  
`Ḷ`: Range `[0..x-1]`  
`Ọ`: Python OR  
`Ŀ`: Edit Distance between strings / lists / integers (automatically converts to digits)  
`Ḃ`: Binary digits -> Integer  
`Ḋ`: Decimal digits -> Integer  
`‘`: Increment  
`’`: Decrement  
