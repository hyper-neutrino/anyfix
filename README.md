# anyfix

Anyfix was inspired by Jelly and 05AB1E, two of my favorite golfing languages made by Dennis and Adnan (PPCG), respectively. It uses the Jelly SBCS. It was designed to support prefix, infix, postfix, or any combination of the three, by waiting for there to be enough arguments before applying an operation (instead of throwing errors) but because of that, dyads and above default to prefix and monads default to postfix. As soon as any of the operators have enough arguments, the first one in the program will be executed, and it will update again to see if any others can run because of the update.

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
`(1 2 3)`: splat (that is, all elements returned by its evaluation will be pushed independently onto the stack). Useful for overriding order of operations

## codeblocks
`ßcode»`: sort over a key function. If top-of-stack is a list, sort that; otherwise, sort the whole stack  
`Ɓcode»`: sort the stack over a key function, even if the top of the stack is a list  
`€code»`: map over a key function. If top-of-stack is a list, map that; otherwise, map the whole stack  
`£code»`: map the stack over a key function, even if the top of the stack is a list  
`þcode»`: filter over a key function. If top-of-stack is a list, filter that; otherwise, filter the whole stack  
`ʠcode»`: filter out over a key function. If top-of-stack is a list, filter out that; otherwise, apply on the whole stack  
`/code»`: reduce over a key (dyadic) function  
`\code»`: reduce over a key (dyadic) function, keeping intermediate results  
`¿code»`: while loop; look at the top of the stack each time and if stack is non-empty and the top value is true, run the code on the stack  
`¢code»`: while loop; pop the top of the stack each time and if stack is non-empty and the popped value is true, run the code on the stack
`¡code»`: while loop; keep running the code until the elements are no longer unique  

Codeblocks do not need the trailing '»'; that's only required for if `code` contains more than one token.  

## commands
`©`: Copy top of stack to register  
`¬`: Logical inverse  
`®`: Push register  
`½`: Square Root  
`Æ½`: Integer Square Root  
`×`: Multiply  
`ı`: Complex Number  
`ȷ`: `1-from-top * 10 ** top` (exp-10)  
`÷`: Float Division  
`!`: Factorial / Pi Function  
`"`: Duplicate top of stack  
`#`: Parse to integer or float  
`&`: Logical AND  
`*`: Exponentiation  
`+`: Addition (Integer, String, List Element-wise, Integer into List on each element)  
`-`: Negate (Integer)  
`:`: Integer Division  
`;`: Concatenate. Implicitly calls converts from integers to strings  
`<`: Less Than  
`=`: Equality Check  
`>`: Greater Than  
`?`: Ternary: `2-from-top if top else 1-from-top`  
`@`: Pop the top of the stack into the register  
`A`: Absolute Value  
`B`: Integer -> Binary Digits, or String -> Characters; does nothing to multi-value things
`D`: Integer -> Decimal Digits, or String -> Characters; does nothing to multi-value things  
`F`: Flatten Array  
`I`: Differences between elements  
`J`: Range of Length (according to `L`)  
`K`: Join by space  
`L`: Length; converts numbers to strings automatically  
`O`: String -> Map to code-points, Character -> code-point, Integer -> character at that code-point  
`P`: Product  
`R`: Range `[1..x]`  
`S`: Sum  
`U`: Reverses the top if it can be iterated over; otherwise, the whole stack  
`X`: Expand the top of the stack to individual elements; does nothing if the top is not iterable  
`_`: Subtraction; `1-from-top - top`  
`b`: Convert from number to digits in specified base  
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
`⁽`: Move the top of the stack to the bottom  
`⁾`: Move the bottom of the stack to the top  
`Ƒ`: Find the start and end of all matches of the pattern `1-from-top` in the string `top`  
`Ɠ`: Evaluate a single line of input  
`Ɱ`: Determine whether or not the pattern `1-from-top` matches the start of the string `top`  
`Ɲ`: Finds the end of the match of the pattern `1-from-top` in the string `top` if it matches; otherwise, 0  
`Ƥ`: Print followed by a newline  
`ƈ`: Read a single character of input  
`ƒ`: Find all substrings of `top` that match pattern `1-from-top`, non-overlapping  
`ɠ`: Read a line of input  
`ɦ`: Read all input into a list of lines  
`ƥ`: Print not followed by a newline  
`ʂ`: Replace all occurrences of the pattern `2-from-top` with `1-from-top` in the string `top`  
`Ạ`: Python AND  
`Ḅ`: Bit (`x % 2`)  
`İ`: Reverse increments; cumulatively add all of the elements of the array `top` to the element `1-from-top`. `1 10R İ` is equivalent to `10R \+ +1`  
`Ḷ`: Range `[0..x-1]`  
`Ọ`: Python OR  
`Ḃ`: Binary digits -> Integer  
`Ḋ`: Decimal digits -> Integer  
`Ŀ`: Edit Distance between strings / lists / integers (automatically converts to digits)  
`ḅ`: Convert list to number using specified base  
`‘`: Increment  
`’`: Decrement  

## examples
`“Hello, World!”` - prints `"Hello, World!"`. Heh, very boring.  
(more to come later
