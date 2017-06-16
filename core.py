from math import *

class splat():
    def __init__(self, array):
        self.array = array
        self.__name__ = 'splat'

def basedigits(number, base):
    return [(number % base ** (k + 1)) // (base ** k) for k in range(ceil(log(number, base)))[::-1]] if type(number) == type(0) else list(number) if number == str(number) else number

def unbase(digits, base):
    return sum(digits[i] * base ** (len(digits) - i - 1) for i in range(len(digits)))
