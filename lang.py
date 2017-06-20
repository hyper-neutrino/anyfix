from core import *
from sympy import *
import arities, sys, functools, operator, re, math

code_page  = '''¡¢£¤¥¦©¬®µ½¿€ÆÇÐÑ×ØŒÞßæçðıȷñ÷øœþ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~¶'''
code_page += '''°¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ƁƇƊƑƓƘⱮƝƤƬƲȤɓƈɗƒɠɦƙɱɲƥʠɼʂƭʋȥẠḄḌẸḤỊḲḶṂṆỌṚṢṬỤṾẈỴẒȦḂĊḊĖḞĠḢİĿṀṄȮṖṘṠṪẆẊẎŻạḅḍẹḥịḳḷṃṇọṛṣṭụṿẉỵẓȧḃċḋėḟġḣŀṁṅȯṗṙṡṫẇẋẏż«»‘’“”'''
escapemap  = '''¡¢£¤¥¦©¬®µ½¿€ÆÇÐÑ×ØŒÞßæçðıȷñ÷øœþ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`a\bcdefghijklm\nopq\rs\tuvwxyz{|}~¶'''
escapemap += '''°¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ƁƇƊƑƓƘⱮƝƤƬƲȤɓƈɗƒɠɦƙɱɲƥʠɼʂƭʋȥẠḄḌẸḤỊḲḶṂṆỌṚṢṬỤṾẈỴẒȦḂĊḊĖḞĠḢİĿṀṄȮṖṘṠṪẆẊẎŻạḅḍẹḥịḳḷṃṇọṛṣṭụṿẉỵẓȧḃċḋėḟġḣŀṁṅȯṗṙṡṫẇẋẏż«»‘’“”'''

class splat():
    def __init__(self, array, force = False):
        self.array = list(array)
        self.force = force
        self.__splat__ = True

class actualNone():
    def __init__(self):
        pass

functions = {
    '¡': lambda: 0,
    '¢': lambda: 0,
    '£': lambda: 0,
    '¤': lambda: 0,
    '¥': lambda x, y: stringify(y, sigdig = x, chop = True),
    '¦': lambda: 0,
    '©': lambda x: setRegister(x),
    '¬': lambda x: not x,
    '®': lambda: getRegister(),
    'µ': lambda: 0,
    '½': lambda x: requireSingularMonadicNumberOperator(sqrt, x, len, None, None),
    'Æ½': lambda x: requireSingularMonadicNumberOperator(lambda x: int(sqrt(x)), x, len, None, None),
    'Ç': lambda x, y: splat([y, x, y], force = True),
    'Ð': lambda x: splat([clone(x), clone(x), clone(x)], force = True),
    'Ñ': lambda: 0,
    '×': lambda x, y: multiply(y, x),
    'Ø': lambda x, y: padDefaultCentre(forceList(y), x),
    'ç': lambda x, y: splat([clone(y) for i in range(x)], force = True),
    'ð': lambda: 0,
    'ı': lambda x, y: y + x * 1j,
    'ȷ': lambda x, y: y * 10 ** x,
    'ñ': lambda: 0,
    '÷': lambda x, y: divide(y, x),
    'ø': lambda x, y, z: padcentre(forceList(z), y, forceList(x)),
    ' ': lambda: 0,
    '!': lambda x: Pi(x),
    '"': lambda x: splat([clone(x), clone(x)], force = True),
    '#': lambda x: x if isNumber(x) else Number(x),
    '$': lambda x: stringify(x),
    '%': lambda x, y: y % x,
    '&': lambda x, y: True if y and x else False,
    '\'': lambda: 0,
    '*': lambda x, y: exponentiate(y, x),
    '+': lambda x, y: addition(y, x),
    ',': lambda: 0,
    '-': lambda x: -x,
    '.': lambda: 0,
    ':': lambda x, y: intdivide(y, x),
    ';': lambda x, y: append(y, x),
    '<': lambda x, y: requireSingularDyadicNumberOperator(lambda x, y: x < y, y, x, lambda x: True, lambda x: False, len, None),
    '=': lambda x, y: x == y,
    '>': lambda x, y: requireSingularDyadicNumberOperator(lambda x, y: x < y, x, y, lambda x: True, lambda x: False, len, None),
    '?': lambda x, y, z: z if x else y,
    '@': lambda x: setRegisterNoReturn(x),
    'A': lambda x: requireSingularMonadicNumberOperator(abs, x, len, None, None),
    'B': lambda x: requireSingularMonadicNumberOperator(lambda x: basedigits(x, 2), x, len, None, None),
    'C': lambda: 0,
    'D': lambda x: requireSingularMonadicNumberOperator(lambda x: basedigits(x, 10), x, len, None, None),
    'E': lambda: 0,
    'F': lambda *a: splat(flatten(a)),
    'G': lambda: 0,
    'H': lambda: 0,
    'I': lambda *a: [a[i] - a[i - 1] for i in range(1, len(a))],
    'J': lambda x: list(range(1, 1 + len(x if hasattr(x, '__getitem__') else str(x)))),
    'K': lambda *a: ' '.join(map(str, a)),
    'L': lambda x: Integer(len(x if hasattr(x, '__getitem__') else str(x))),
    'M': lambda: 0,
    'N': lambda: 0,
    'O': lambda x: (list(map(ord, x)) if len(x) > 1 else ord(x)) if hasattr(x, '__getitem__') else chr(int(x)),
    'P': lambda *a: reduce(multiply, a),
    'Q': lambda: 0,
    'R': lambda x: list(map(Rational, range(1, int(1 + x)))),
    'S': lambda *a: reduce(addition, a),
    'T': lambda: 0,
    'U': lambda *a: splat(a[::-1]),
    'V': lambda *a: [a[0] if isNumber(a[0]) else evaluate(''.join(a[0]) if type(a) == type([]) else a[0], a[1:])] + a[1:],
    'W': lambda x: [x],
    'X': lambda *a: splat(a, force = True),
    'Y': lambda *a: '\n'.join(map(str, a)),
    'Z': lambda a: list(map(list, zip(a))),
    '^': lambda x, y: requireSingularDyadicNumberOperator(lambda x, y: x ^ y, y, x, lambda x: x, lambda x: x, mapper(ord), None, int),
    '_': lambda x, y: subtract(y, x),
    '`': lambda: 0,
    'a': lambda: 0,
    'b': lambda x, y: requireSingularMonadicNumberOperator(lambda k: basedigits(k, x), y, len, None, None),
    'c': lambda: 0,
    'd': lambda: 0,
    'e': lambda: 0,
    'f': lambda: 0,
    'g': lambda: 0,
    'h': lambda: 0,
    'i': lambda: 0,
    'j': lambda x, y: y.join(map(str, x)),
    'k': lambda: 0,
    'l': lambda: 0,
    'm': lambda: 0,
    'n': lambda: 0,
    'o': lambda: 0,
    'p': lambda x, y: padDefaultLeft(forceList(y), x),
    'q': lambda x, y: padDefaultRight(forceList(y), x),
    'r': lambda: 0,
    's': lambda x, y: blocks(y, x),
    't': lambda: 0,
    'u': lambda: 0,
    'v': lambda: 0,
    'w': lambda: 0,
    'x': lambda x, y: repeat(y, x),
    'y': lambda: 0,
    'z': lambda x, y: padzip(y, x),
    '{': lambda x, y, z: padleft(forceList(z), y, forceList(x)),
    '|': lambda x, y: True if y or x else False,
    '}': lambda x, y, z: padright(forceList(z), y, forceList(x)),
    '~': lambda: 0,
    '¶': lambda: 0,
    '°': lambda: 0,
    '¹': lambda x: x,
    '²': lambda x: x ** 2,
    '³': lambda: Integer(16),
    '⁴': lambda: Integer(10),
    '⁵': lambda: Integer(100),
    '⁶': lambda: ' ',
    '⁷': lambda: '',
    '⁸': lambda: '\n',
    '⁹': lambda: [],
    '⁺': lambda *a: splat(recursiveFilter(lambda x: x > 0, a, True)),
    '⁻': lambda *a: splat(recursiveFilter(lambda x: isNumber(x) and x < 0, a, False)),
    '⁼': lambda x, y: type(x) == type(y),
    '⁽': lambda *a: splat(a[1:] + a[:1], force = True),
    '⁾': lambda *a: splat(a[-1:] + a[:-1], force = True),
    'Ƈ': lambda: 0,
    'Ɗ': lambda: 0,
    'Ƒ': lambda x, y: allSpans(y, x),
    'Ɠ': lambda: eval(input()),
    'Ƙ': lambda: 0,
    'Ɱ': lambda x, y: bool(re.match(y, x)),
    'Ɲ': lambda x, y: re.match(y, x).end() if re.match(y, x) else 0,
    'Ƥ': lambda x: print(x),
    'Ƭ': lambda x, y: y.split(x),
    'Ʋ': lambda *a: list(a[1:a[0] + 1]) + [a[1]] + list(a[a[0] + 1:]),
    'Ȥ': lambda *a: [a[a[0]]] + list(a[1:]),
    'ɓ': lambda: 0,
    'ƈ': lambda: sys.stdin.read(1),
    'ɗ': lambda: 0,
    'ƒ': lambda x, y: re.findall(y, x),
    'ɠ': lambda: input(),
    'ɦ': lambda: exhaustInput(),
    'ƙ': lambda: exhaustInputSingleString(),
    'ɱ': lambda: splat(list(map(eval, exhaustInput()))),
    'ɲ': lambda: 0,
    'ƥ': lambda x: print(x, end = ''),
    'ɼ': lambda x, y, z: z.replace(x, y),
    'ʂ': lambda x, y, z: re.sub(x, y, z),
    'ƭ': lambda x, y: re.split(y, x),
    'ʋ': lambda *a: list(a[2:a[0] + 1]) + [a[1]] + list(a[a[0] + 1:]),
    'ȥ': lambda *a: [a[a[0]]] + list(a[1:a[0]]) + list(a[a[0]+1:]),
    'Ạ': lambda x, y: y and x,
    'Ḅ': lambda x: x % 2,
    'Ḍ': lambda: 0,
    'Ẹ': lambda: 0,
    'Ḥ': lambda: 0,
    'Ị': lambda: 0,
    'Ḳ': lambda: 0,
    'Ḷ': lambda x: list(range(x)),
    'Ṃ': lambda: 0,
    'Ṇ': lambda: 0,
    'Ọ': lambda x, y: y or x,
    'Ṛ': lambda: 0,
    'Ṣ': lambda: 0,
    'Ṭ': lambda: 0,
    'Ụ': lambda: 0,
    'Ṿ': lambda: 0,
    'Ẉ': lambda: 0,
    'Ỵ': lambda: 0,
    'Ẓ': lambda: 0,
    'Ȧ': lambda: 0,
    'Ḃ': lambda x: unbase(x, 2),
    'Ċ': lambda: 0,
    'Ḋ': lambda x: unbase(x, 10),
    'Ė': lambda: 0,
    'Ḟ': lambda: 0,
    'Ġ': lambda: 0,
    'Ḣ': lambda: 0,
    'İ': lambda x, y: [y + sum(x[:i]) for i in range(1, len(x) + 1)],
    'Ŀ': lambda x, y: levenshtein(castIterable(x), castIterable(y)),
    'Ṁ': lambda: 0,
    'Ṅ': lambda: 0,
    'Ȯ': lambda: 0,
    'Ṗ': lambda: 0,
    'Ṙ': lambda: 0,
    'Ṡ': lambda: 0,
    'Ṫ': lambda: 0,
    'Ẇ': lambda: 0,
    'Ẋ': lambda: 0,
    'Ẏ': lambda: 0,
    'Ż': lambda: 0,
    'ạ': lambda: 0,
    'ḅ': lambda x, y: unbase(y, x),
    'ḍ': lambda: 0,
    'ẹ': lambda: 0,
    'ḥ': lambda: 0,
    'ị': lambda: 0,
    'ḳ': lambda: 0,
    'ḷ': lambda: 0,
    'ṃ': lambda: 0,
    'ṇ': lambda: 0,
    'ọ': lambda: 0,
    'ṛ': lambda: 0,
    'ṣ': lambda: 0,
    'ṭ': lambda: 0,
    'ụ': lambda: 0,
    'ṿ': lambda: 0,
    'ẉ': lambda: 0,
    'ỵ': lambda: 0,
    'ẓ': lambda: 0,
    'ȧ': lambda: 0,
    'ḃ': lambda: 0,
    'ċ': lambda: 0,
    'ḋ': lambda: 0,
    'ė': lambda: 0,
    'ḟ': lambda: 0,
    'ġ': lambda x, y: gcd(x, y),
    'ḣ': lambda: 0,
    'ŀ': lambda x, y: x * y / gcd(x, y),
    'ṁ': lambda: 0,
    'ṅ': lambda: 0,
    'ȯ': lambda: 0,
    'ṗ': lambda: 0,
    'ṙ': lambda: 0,
    'ṡ': lambda: 0,
    'ṫ': lambda: 0,
    'ẇ': lambda: 0,
    'ẋ': lambda x, y: repeatIter(forceList(y), x),
    'ẏ': lambda: 0,
    'ż': lambda: 0,
    '«': lambda x, y: splat([y, x], force = True),
    '‘': lambda x: x + 1,
    '’': lambda x: x - 1,
}

codeblock_tokens = {
    'ß': 'BlockSortToken',
    'Ɓ': 'BlockStackSortToken',
    '€': 'BlockMapToken',
    '£': 'BlockStackMapToken',
    'þ': 'BlockFilterToken',
    'ʠ': 'BlockFilterOutToken',
    '/': 'BlockReduceToken',
    '\\': 'BlockReduceCumulativeToken',
    '¿': 'ConditionalWhileToken',
    '¢': 'ConditionalPopWhileToken',
    '¡': 'ConditionalUniqueWhileToken'
}

extenders = ['Æ', 'Œ', 'æ', 'œ']

bracket_closers = {
    '[': ']',
    '(': ')'
}

multitokens = {
    '[': 'MultivalueListToken',
    '(': 'MultivalueSplatToken'
}

multivalue_converters = {
    'MultivalueListToken': list,
    'MultivalueSplatToken': splat
}

def round(number, precision):
    number = number + precision / 2 - (number + precision / 2) % precision
    if number % 1 == 0:
        return int(number)
    else:
        return number

def rounder(precision):
    return lambda number: round(number, precision)

def basedigits(number, base):
    if number > 0:
        if base == 1: return [1] * int(number)
        digits = []
        start = int(log(number, base))
        while start + 1:
            if start:
                digits.append(Integer(number / (base ** start)))
                number %= base ** start
            start -= 1
        return digits + [number]
    elif number == 0:
        return [0]
    else:
        return [-x for x in basedigits(-number, base)]

def unbase(digits, base):
    return Integer(len(digits)) if base == 1 else Rational(sum(digits[i] * base ** (len(digits) - i - 1) for i in range(len(digits))))

def castMultivalue(ref, apply):
    if type(apply) == type(ref):
        return apply
    elif type(ref) == type([]):
        return list(apply)
    else:
        return apply

def recursiveFilter(condition, array, bypass_strings):
    result = []
    for value in array:
        if type(value) == type('') and bypass_strings:
            result.append(value)
        elif hasattr(value, '__getitem__'):
            result.append(recursiveFilter(condition, array))
        else:
            if condition(value):
                result.append(value)
    return result

def isIterable(x):
    return hasattr(x, '__getitem__') or hasattr(x, '__iter__')

def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

def castIterable(value):
    if hasattr(value, '__iter__') or hasattr(value, '__getitem__'):
        return list(value)
    else:
        return basedigits(int(value), 10)

register = 0

def setRegister(value):
    global register
    register = value
    return value

def setRegisterNoReturn(value):
    setRegister(value)
    return None

def getRegister():
    global register
    return register

def repeat(array, times):
    result = []
    for value in array:
        for i in range(times):
            result.append(value)
    return castMultivalue(array, result)

def Pi(number):
	if type(number) < Integer:
		if number < 0:
			return inf
		try:
			return math.factorial(number)
		except:
			return functools.reduce(operator.mul, range(1, number + 1), 1)
	return math.gamma(number + 1)

def exhaustInput():
    result = []
    line = input()
    while line:
        result.append(line)
        line = input()
    return result

def exhaustInputSingleString():
    return '\n'.join(exhaustInput())

def flatten(array):
    result = []
    for value in array:
        if isIterable(value) and type(value) != type(''):
            result += flatten(value)
        else:
            result.append(value)
    return result

def isNumber(x):
    return type(x) < Number or type(x) == Number

def addition(x, y):
    if isNumber(x) and isNumber(y):
        return x + y
    elif type(x) == type('') and type(y) == type(''):
        result = ''
        for index in range(max(len(x), len(y))):
            if index < len(x):
                result += x[index]
            if index < len(y):
                result += y[index]
        return result
    elif isIterable(x) and isIterable(y):
        result = []
        for index in range(max(len(x), len(y))):
            if index < len(x):
                if index < len(y):
                    result.append(addition(x[index], y[index]))
                else:
                    result.append(x[index])
            else:
                result.append(y[index])
        return result
    elif type(x) == type('') and isNumber(y) or type(y) == type('') and isNumber(x):
        return str(x) + str(y)
    elif isIterable(x):
        return addition(x, [y] * len(x))
    elif isIterable(y):
        return addition([x] * len(y), y)

def subtract(x, y):
    if isNumber(x) and isNumber(y):
        return x - y
    elif type(x) == type('') and type(y) == type(''):
        return ''.join(k for k in x if k not in y)
    elif isIterable(x) and isIterable(y):
        result = []
        for index in range(max(len(x), len(y))):
            if index < len(x):
                if index < len(y):
                    result.append(subtract(x[index], y[index]))
                else:
                    result.append(x[index])
            else:
                result.append(y[index])
        return result
    elif type(x) == type('') and isNumber(y):
        return x[:-y]
    elif type(y) == type('') and isNumber(x):
        return y[:-x]
    elif isIterable(x):
        return subtract(x, [y] * len(x))
    elif isIterable(y):
        return subtract([x] * len(y), y)

def repeatIter(iter, times):
    increment = Rational(1, len(iter))
    times = floor(times / increment) * increment
    current = S.Zero
    result = []
    index = 0
    while current < times:
        result.append(iter[index])
        index += 1
        index %= len(iter)
        current += increment
    return ''.join(result) if type(iter) == type('') else result

def multiply(x, y):
    if isNumber(x) and isNumber(y):
        return x * y
    elif isIterable(x) and isIterable(y):
        result = []
        for index in range(max(len(x), len(y))):
            if index < len(x):
                if index < len(y):
                    result.append(multiply(x[index], y[index]))
                else:
                    result.append(x[index])
            else:
                result.append(y[index])
        return result
    elif type(x) == type('') and isNumber(y):
        return repeatStr(x, y)
    elif type(y) == type('') and isNumber(x):
        return repeatStr(y, x)
    elif isIterable(x):
        return multiply(x, [y] * len(x))
    elif isIterable(y):
        return multiply([x] * len(y), y)

def divide(x, y):
    return multiply(x, 1 / y)

def intdivide(x, y):
    return multiply(x, 1 // y)

def requireSingularDyadicNumberOperator(function, x, y, default_x_absent, default_y_absent, string_transformer, string_function, num_preprocessor):
    if isNumber(x) and isNumber(y):
        return function(num_preprocessor(x), num_preprocessor(y)) if num_preprocessor else function(x, y)
    elif type(x) == type('') and type(y) == type(''):
        if string_transformer:
            return requireSingularDyadicNumberOperator(function, string_transformer(x), string_transformer(y), default_x_absent, default_y_absent, string_transformer, string_function, num_preprocessor)
        else:
            return string_function(x, y)
    elif isIterable(x) and isIterable(y):
        result = []
        for index in range(min(len(x), len(y))):
            if index < len(x):
                if index < len(y):
                    result.append(function(x[index], y[index]))
                else:
                    result.append(default_y_absent(x))
            else:
                result.append(default_x_absent(y))
        return result
    elif isIterable(x):
        return requireSingularDyadicNumberOperator(function, x, [y] * len(x), default_x_absent, default_y_absent, string_transformer, string_function, num_preprocessor)
    elif isIterable(y):
        return requireSingularDyadicNumberOperator(function, [x] * len(y), y, default_x_absent, default_y_absent, string_transformer, string_function, num_preprocessor)

def exponentiate(x, y):
    if isNumber(x) and isNumber(y):
        return x ** y
    else:
        ax = x
        for i in range(int(y)):
            x *= ax
        return x

def clone(x):
    if isNumber(x):
        return x
    if isIterable(x):
        if type(x) == type(''):
            return x
        else:
            return [clone(k) for k in x]
    else:
        return x

def append(x, y):
    if isIterable(x) and isIterable(y):
        return x + y
    elif isIterable(x):
        if type(x) == type(''):
            return x + str(y)
        else:
            x = clone(x)
            x.append(y)
            return x
    elif isIterable(y):
        if type(y) == type(''):
            return str(x) + y
        else:
            y = clone(y)
            y.insert(0, x)
            return y
    else:
        return str(x) + str(y)

def cumulativeReduce(function, array):
    for index in range(1, len(array)):
        array[index] = function(array[index], array[index - 1])
    return array

def reduce(reductor, array):
    while len(array) > 1:
        array = [reductor(array[1], array[0])] + list(array[2:])
    return array[0]

def allSpans(pattern, string):
    deleted = 0
    spans = []
    match = re.search(pattern, string)
    while match:
        spans.append([match.start() + deleted + 1, match.end() + deleted + 1])
        deleted += match.end()
        match = re.search(pattern, string[deleted:])
    return spans

def stringify(thing, appx = False):
    if isIterable(thing) and thing != str(thing):
        return ''.join([stringify(subthing, appx = appx) for subthing in thing])
    else:
        if isNumber(thing) and appx:
            return re.sub('0+$', '', str(thing.evalf()))
        else:
            return str(thing)

def listify(thing, appx = False):
    if isIterable(thing) and thing != str(thing):
        return '[' + ', '.join([listify(subthing, appx = appx) for subthing in thing]) + ']'
    else:
        if isNumber(thing) and appx:
            return re.sub('0+$', '', str(thing.evalf()))
        else:
            return str(thing)

def blocks(array, length):
    result = []
    while array:
        result.append(array[:min(length, len(array))])
        array = array[min(length, len(array)):]
    return result

def makeIterable(item, string = True):
    if isIterable(item) and (string or type(item) == type([])):
        return item
    elif isNumber(item):
        return list(range(int(item)))
    else:
        return list(item)

def forceList(item):
    if isIterable(item):
        return list(item)
    else:
        return [item]

def requireSingularMonadicNumberOperator(function, item, string_transformer, string_function, num_preprocessor, string = True):
    if isIterable(item) and (string or type(item) != type('')):
        return list(map(function, list(item)))
    else:
        return function(num_preprocessor(item) if num_preprocessor else item) if isNumber(item) else requireSingularMonadicNumberOperator(function, string_transformer(item), string_transformer, string_function, num_preprocessor, string = string) if string_transformer else string_function(item)

def mapper(function):
    return lambda x: list(map(function, x))

def padleft(iterable, length, filler):
    return repeatIter(filler, (length - len(iterable)) / len(filler)) + iterable

def padright(iterable, length, filler):
    return iterable + repeatIter(filler, (length - len(iterable)) / len(filler))

def padcentre(iterable, length, filler):
    return padleft(padright(iterable, int(len(iterable) + (length - len(iterable)) / 2), filler), int(length), filler)

def padDefaultLeft(iterable, length):
    return padleft(iterable, length, ' ' if type(iterable) == type('') else [S.Zero])

def padDefaultRight(iterable, length):
    return padright(iterable, length, ' ' if type(iterable) == type('') else [S.Zero])

def padDefaultCentre(iterable, length):
    return padcentre(iterable, length, ' ' if type(iterable) == type('') else [S.Zero])

def zip(array):
    result = []
    width = max(map(len, array))
    for index in range(width):
        result.append([])
        for j in range(len(array)):
            if index < len(array[j]):
                result[-1].append(array[j][index])
    return result

def padzip(array, filler):
    result = []
    width = max(map(len, array))
    for index in range(width):
        result.append([])
        for j in range(len(array)):
            if index < len(array[j]):
                result[-1].append(array[j][index])
            else:
                result[-1].append(filler)
    return result

def debug(text):
    if verbose:
        print(text)

def escape(char):
    return escapemap[code_page.find(char)]

def unescape(char):
    return '\\' + code_page[escapemap.find(char)]

def unescapify(string):
    return string if type(string) != type('') else ''.join([char if char in code_page else unescape(char) for char in string])

def baseconvert(string, base):
    if '.' in string:
        left = string.split('.')[0]
        left = len(left) if base == 1 else len(left) and int(left, base)
        right = string.split('.')[1]
        return left + (len(right) if base == 1 else len(right) and int(right, base)) / base ** len(right)
    return int(string, base)

class Token():
    def __init__(self, type, content):
        self.type = type
        self.content = content
    def __str__(self):
        return '%s@{%s}' % (self.type, unescapify(self.content))
    def __repr__(self):
        return self.__str__()
    def isLiteral(self):
        return self.type.startswith('Literal')
    def isMultivalue(self):
        return self.type.startswith('Multivalue')
    def isBlock(self):
        return self.type.startswith('Block')
    def isBlockStack(self):
        return self.type.startswith('BlockStack')
    def isInstruction(self):
        return self.type.startswith('Instruction')
    def isCombo(self):
        return self.type.startswith('Combo')
    def isConditional(self):
        return self.type.startswith('Conditional')
    def isBlockToker(self):
        return self.isBlock() or self.isConditional()

class Tokenizer():
    def __init__(self, code):
        self.code = code.strip()
        self.index = 0
        self.tokens = []
    def tokenize(code):
        tokenizer = Tokenizer(code)
        while tokenizer.hasNext(): tokenizer.next()
        return tokenizer.tokens
    def hasNext(self):
        return self.index < len(self.code)
    def advance(self):
        self.index += 1
        return self.index - 1
    def current(self):
        return self.code[self.index]
    def take(self):
        self.next()
        token = self.tokens[-1]
        self.tokens = self.tokens[:-1]
        return token
    def peek(self):
        index = self.index
        self.advance()
        token = self.take()
        self.index = index
        return token
    def next(self):
        debug('( Now on $%s$ )' % self.current())
        if self.current() == ' ':
            self.advance()
            debug('( Tokenskip )')
            self.next()
        elif self.current() == '“':
            self.advance()
            strings = ['']
            while self.current() != '”':
                if self.current() == '\\':
                    strings[-1] += escape(self.code[self.index + 1])
                    self.advance()
                else:
                    if self.current() == '“':
                        strings.append('')
                    else:
                        strings[-1] += self.current()
                self.advance()
            self.advance()
            self.tokens.append(Token('LiteralStringToken', strings[0]) if len(strings) == 1 else Token('MultivalueListToken', [Token('LiteralStringToken', string) for string in strings]))
        elif self.current() == '”':
            self.advance()
            if self.current() == '\\':
                self.advance()
                self.tokens.append(Token('LiteralStringToken', escape(self.code[self.advance()])))
            else:
                self.tokens.append(Token('LiteralStringToken', self.code[self.advance()]))
        elif self.current() in '0123456789.':
            decimal = False
            number = ''
            while self.hasNext():
                if self.current() in '0123456789' or self.current() == '.' and not decimal:
                    if self.current() == '.': decimal = True
                    number += self.current()
                    self.advance()
                else:
                    break
            self.tokens.append(Token('LiteralNumberToken', Rational(number)))
        elif self.current() in bracket_closers:
            array = []
            opener = self.current()
            closer = bracket_closers[opener]
            self.advance()
            while self.hasNext() and self.current() != closer:
                array.append(self.take())
            self.advance()
            self.tokens.append(Token(multitokens[opener], array))
        elif self.current() in codeblock_tokens:
            self.tokens.append(Token(codeblock_tokens[self.current()], ''))
            self.advance()
        elif self.current() == '»':
            tokenlist = []
            buffer = 0
            while buffer or not self.tokens[-1].isBlockToker():
                debug('( Token Grouper found token %s )' % str(self.tokens[-1]))
                tokenlist = [self.tokens[-1]] + tokenlist
                self.tokens = self.tokens[:-1]
                debug('( Token list is now %s )' % str(self.tokens))
                if tokenlist[0].isCombo():
                    buffer += 1
                elif tokenlist[0].isBlockToker():
                    buffer -= 1
            self.tokens.append(Token('ComboToken', tokenlist))
            self.advance()
        elif self.current() in extenders:
            extender = self.current()
            self.advance()
            self.tokens.append(Token('InstructionToken', extender + self.code[self.advance()]))
        else:
            self.tokens.append(Token('InstructionToken', self.code[self.advance()]))
        debug('Token List: %s' % str(self.tokens))

class Interpreter():
    def __init__(self, tokens):
        self.tokens = tokens
        self.instruction_queue = []
        self.mem = []
    def operate(tokens, mem):
        debug('( Operating on %s )' % str(tokens))
        interpreter = Interpreter(tokens)
        interpreter.mem = mem
        debug('( Interpreter initialized with mem %s and tokens %s )' % (str(interpreter.mem), str(interpreter.tokens)))
        while interpreter.hasNext(): interpreter.next(); debug('( Stack is now %s )' % str(interpreter.mem))
        return interpreter.mem[::-1]
    def evaluate(code, mem):
        return Interpreter.operate(Tokenizer.tokenize(code), mem)
    def nextToken(self):
        return self.tokens[0]
    def peek(self):
        return self.mem[0]
    def count(self, count):
        return self.mem[:count]
    def pop(self):
        front = self.peek()
        self.mem = self.mem[1:]
        return front
    def popCount(self, count):
        front = self.count(count)
        self.mem = self.mem[count:]
        return front
    def popAll(self):
        return self.popCount(len(self.mem))
    def push(self, value):
        if value == None:
            pass
        elif type(value) == type(actualNone()):
            self.mem = [None] + self.mem
        elif hasattr(value, '__splat__') and value.__splat__:
            if value.force:
                self.pushAll(*value.array)
            else:
                self.mem = [list(value.array)] + self.mem
        elif type(value) == type(0):
            self.mem = [Integer(value)] + self.mem
        elif type(value) == type(0.5):
            self.mem = [Rational(value)] + self.mem
        else:
            self.mem = [value] + self.mem
        return self
    def pushAll(self, *values):
        for value in values[::-1]:
            self.push(value)
    def hasNext(self):
        return bool(self.tokens)
    def update(self):
        if self.instruction_queue:
            for i in range(len(self.instruction_queue)):
                token = self.instruction_queue[i]
                arity = arities.arities[token.content]
                if len(self.mem) >= arity:
                    debug('( %s operates with enough items on stack after push )' % str(token))
                    function = functions[token.content]
                    arguments = self.popCount(arity)
                    self.push(function(*arguments))
                    self.instruction_queue = self.instruction_queue[:i] + self.instruction_queue[i + 1:]
                    self.update()
    def next(self):
        token = self.tokens[0]
        self.tokens = self.tokens[1:]
        debug('Tokens Left: %s' % str(self.tokens))
        debug('Evaluating %s' % str(token))
        if token.isLiteral():
            debug('( Literal token )')
            self.push(token.content)
        elif token.isMultivalue():
            debug('( Multivalue token )')
            tokenlist = token.content
            valuelist = Interpreter.operate(tokenlist, [])
            self.push(multivalue_converters[token.type](valuelist))
        elif token.isInstruction() and all(char in code_page for char in token.content):
            debug('( Instruction Token )')
            arity = arities.arities[token.content]
            debug('( Arity %d )' % arity)
            if arity == -1:
                debug('( Operates over entire stack )')
                function = functions[token.content]
                arguments = self.popAll()
                self.push(function(*arguments))
            elif arity <= -2:
                debug('( Operates over iterable )')
                if self.mem:
                    function = functions[token.content]
                    result = []
                    top = None
                    if isIterable(self.peek()) and (arity != -3 or type(self.peek()) != type('')):
                        top = self.pop()
                        result = function(*top)
                    else:
                        result = function(*self.popAll())
                        if top != None:
                            if (hasattr(result, '__splat__') and result.__splat__) and not result.force: result = result.array
                            if type(top) != type(result) and isIterable(result):
                                if type(top) == type(''):
                                    result = str(result)
                                elif type(top) == type([]):
                                    result = list(result)
                    self.push(result)
            elif len(self.mem) >= arity:
                debug('( Enough items on stack )')
                function = functions[token.content]
                arguments = self.popCount(arity)
                debug('( Arguments %s )' % str(arguments))
                debug('( Function %s )' % str(function))
                self.push(function(*arguments))
            else:
                debug('( Not enough items on stack; adding to queue )')
                self.instruction_queue.append(token)
        elif token.isBlock():
            listmode = not token.isBlockStack() and isIterable(type(self.peek()))
            array = self.pop() if listmode else self.popAll()
            def push(array):
                if listmode: self.push(array)
                else: self.pushAll(*array)
            if token.type.endswith('SortToken'):
                push(list(sorted(array, key = lambda x: Interpreter.operate([self.nextToken()], [x]))))
            elif token.type.endswith('MapToken'):
                push(list(map(lambda x: Interpreter.operate([self.nextToken()], [x])[0], array)))
            elif token.type.endswith('FilterToken'):
                push(list(filter(lambda x: Interpreter.operate([self.nextToken()], [x])[0], array)))
            elif token.type.endswith('FilterOutToken'):
                push(list(filter(lambda x: not Interpreter.operate([self.nextToken()], [x])[0], array)))
            elif token.type.endswith('ReduceToken'):
                push(reduce(lambda x, y: Interpreter.operate([self.nextToken()], [x, y])[0], array))
            elif token.type.endswith('ReduceCumulativeToken'):
                push(cumulativeReduce(lambda x, y: Interpreter.operate([self.nextToken()], [x, y])[0], array))
            self.tokens = self.tokens[1:]
        elif token.isConditional():
            if token.type.endswith('WhileToken'):
                debug('Operating WHILE on stack %s' % str(self.mem))
                getter = self.pop if token.type == 'ConditionalPopWhileToken' else self.peek
                values = []
                condition = (lambda: len(set(map(lambda x: tuple(x) if isIterable(x) else x, values))) == len(values)) if token.type == 'ConditionalUniqueWhileToken' else (lambda: self.mem and getter())
                while condition():
                    self.mem = Interpreter.operate([self.nextToken()], self.mem)
                    values.append(self.mem)
                    debug('Stack after WHILE loop: %s' % str(self.mem))
                self.tokens = self.tokens[1:]
        elif token.isCombo():
            self.mem = Interpreter.operate(token.content, self.mem)
        self.update()
        debug('Stack: %s' % str(self.mem))

verbose = False
listmode = False
givetypes = False
appx = True
arguments = {}

def processFlags(flags):
    global verbose
    global listmode
    global appx
    global givetypes
    verbose = 'v' in flags
    listmode = 'l' in flags
    appx = 'x' not in flags # `x` means `exact`
    givetypes = 't' in flags
    debug('Received flags: %s' % flags)

def evaluate(code, mem):
    tokens = Tokenizer.tokenize(code)
    debug('TOKENS: %s' % str(tokens))

    interpreter = Interpreter(tokens)
    interpreter.mem = mem

    while interpreter.hasNext():
        interpreter.next()

    return interpreter.mem

def typify(mem):
    if type(mem) == type([]):
        return list(map(typify, mem))
    else:
        return (type(mem), mem)

def output(mem, flags, end):
    if givetypes:
        print(typify(mem))
    elif listmode:
        print(listify(mem, appx = appx), end = end)
    else:
        print(stringify(mem, appx = appx), end = end)
