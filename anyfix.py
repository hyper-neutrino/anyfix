from sympy import *
import lang, sys

flag_utf8 = False
end = ''

usage = '''Usage:

    anyfix f <file> [input]   Reads the Anyfix program stored in the
                              specified file, using the Jelly code page.
                              This option should be considered the default,
                              but it exists solely for scoring purposes in
                              code golf contests.

    anyfix fu <file> [input]  Reads the Anyfix program stored in the
                              specified file, using the UTF-8 encoding.

    anyfix e <code> [input]   Reads an Anyfix program as a command line
                              argument, using the Jelly code page. This
                              requires setting the environment variable
                              LANG (or your OS's equivalent) to en_US or
                              compatible.

    anyfix eu <code> [input]  Reads an Anyfix program as a command line
                              argument, using the UTF-8 encoding. This
                              requires setting the environment variable
                              LANG (or your OS's equivalent) to en_US.UTF8
                              or compatible.

    Append an `n` to the flag list to append a trailing newline to the
    program's output.

Visit http://github.com/alexander-liao/anyfix for more information.\n'''

if len(sys.argv) < 3:
    raise SystemExit(usage)

flags = ''

for char in sys.argv[1]:
    if char == 'f':
        flag_file = True
    elif char == 'u':
        flag_utf8 = True
    elif char == 'e':
        flag_file = False
    elif char == 'n':
        end = '\n'
    else:
        flags += char

if flag_file:
	with open(sys.argv[2], 'rb') as file:
		code = file.read()
	if flag_utf8:
		code = ''.join(char for char in code.decode('utf-8').replace('\n', '¶') if char in lang.code_page)
	else:
		code = ''.join(lang.code_page[i] for i in code)
else:
	code = sys.argv[2]
	if flag_utf8:
		code = ''.join(char for char in code.replace('\n', '¶') if char in lang.code_page)
	else:
		code = ''.join(lang.code_page[ord(i)] for i in code)

def anyfix_eval(x):
    pre = eval(x)
    if type(pre) == type(0) or type(pre) == type(0.5):
        return Rational(x)
    elif type(pre) == type([]):
        return list(map(anyfix_eval, map(str, pre)))
    else:
        return str(x)[1:-1]

lang.processFlags(flags)
lang.output(lang.evaluate(code, list(map(anyfix_eval, sys.argv[3:]))), flags, end)
