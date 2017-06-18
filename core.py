from math import *
import functools, operator, anyfix_globals

class splat():
    def __init__(self, array, force = False):
        self.array = list(array)
        self.force = force
        self.__splat__ = True

class actualNone():
    def __init__(self):
        pass

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
        digits = []
        start = int(log(number, base))
        while start + 1:
            if start:
                digits.append(int(number / (base ** start)))
                number %= base ** start
            start -= 1
        return digits + [round(number, anyfix_globals.values['r'])]
    elif number == 0:
        return [0]
    else:
        return [-x for x in basedigits(-number, base)]

def unbase(digits, base):
    return sum(digits[i] * base ** (len(digits) - i - 1) for i in range(len(digits)))

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
	if type(number) == int:
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
    return type(x) == type(0) or type(x) == type(0.5)

def add(x, y):
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
                    result.append(add(x[index], y[index]))
                else:
                    result.append(x[index])
            else:
                result.append(y[index])
        return result
    elif type(x) == type('') or type(y) == type(''):
        return str(x) + str(y)

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
            y = clone(y)
            y.insert(0, x)
            return y
    else:
        return str(x) + str(y)
