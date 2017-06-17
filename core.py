from math import *
import functools
import operator

class splat():
    def __init__(self, array):
        self.array = array
        self.__name__ = 'splat'

class actualNone():
    def __init__(self):
        pass

def basedigits(number, base):
    return [(number % base ** (k + 1)) // (base ** k) for k in range(ceil(log(number, base)))[::-1]] if type(number) == type(0) else list(number) if number == str(number) else number

def unbase(digits, base):
    return sum(digits[i] * base ** (len(digits) - i - 1) for i in range(len(digits)))

def castMultivalue(ref, apply):
    if type(apply) == type(ref):
        return apply
    elif type(ref) == type([]):
        return list(apply)
    elif type(ref) == type(tuple([])):
        return tuple(apply)
    elif type(ref) == type(set([])):
        return set(apply)
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
