from core import *
import arities, functions, sys, anyfix_globals

code_page  = '''¡¢£¤¥¦©¬®µ½¿€ÆÇÐÑ×ØŒÞßæçðıȷñ÷øœþ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~¶'''
code_page += '''°¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ƁƇƊƑƓƘⱮƝƤƬƲȤɓƈɗƒɠɦƙɱɲƥʠɼʂƭʋȥẠḄḌẸḤỊḲḶṂṆỌṚṢṬỤṾẈỴẒȦḂĊḊĖḞĠḢİĿṀṄȮṖṘṠṪẆẊẎŻạḅḍẹḥịḳḷṃṇọṛṣṭụṿẉỵẓȧḃċḋėḟġḣŀṁṅȯṗṙṡṫẇẋẏż«»‘’“”'''
escapemap  = '''¡¢£¤¥¦©¬®µ½¿€ÆÇÐÑ×ØŒÞßæçðıȷñ÷øœþ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`a\bcdefghijklm\nopq\rs\tuvwxyz{|}~¶'''
escapemap += '''°¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ƁƇƊƑƓƘⱮƝƤƬƲȤɓƈɗƒɠɦƙɱɲƥʠɼʂƭʋȥẠḄḌẸḤỊḲḶṂṆỌṚṢṬỤṾẈỴẒȦḂĊḊĖḞĠḢİĿṀṄȮṖṘṠṪẆẊẎŻạḅḍẹḥịḳḷṃṇọṛṣṭụṿẉỵẓȧḃċḋėḟġḣŀṁṅȯṗṙṡṫẇẋẏż«»‘’“”'''

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
            self.tokens.append(Token('LiteralNumberToken', baseconvert(number, base)))
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
        else:
            if type(value) == type(0.5):
                self.mem = [round(value, anyfix_globals.values['r'])] + self.mem
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
                    function = functions.functions[token.content]
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
                function = functions.functions[token.content]
                arguments = self.popAll()
                self.push(function(*arguments))
            elif arity <= -2:
                debug('( Operates over iterable )')
                if self.mem:
                    function = functions.functions[token.content]
                    result = []
                    top = None
                    if isIterable(self.peek()) and (arity == -2 or type(self.peek()) != type('')):
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
                function = functions.functions[token.content]
                arguments = self.popCount(arity)
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

code = ''
code = sys.argv[1]
tokens = Tokenizer.tokenize(code)
debug('TOKENS: %s' % str(tokens))

interpreter = Interpreter(tokens)

for index in range(2, len(sys.argv)):
    if sys.argv[index].startswith('@'):
        key = sys.argv[index][1]
        if key in anyfix_globals.values:
            anyfix_globals.setGlobal(key, anyfix_globals.typers[key](sys.argv[index][2:]))
    else:
        interpreter.mem.append(eval(sys.argv[index]))

interpreter.mem = interpreter.mem[::-1]

while interpreter.hasNext():
    interpreter.next()

if '@list' in sys.argv or '@l' in sys.argv:
    print('[', end = '')
    for index in range(len(interpreter.mem)):
        print(interpreter.mem[index], end = ('' if index == len(interpreter.mem) - 1 else ', '))
    print(']')
elif '@spaced' in sys.argv or '@s' in sys.argv:
    print(' '.join(map(str, interpreter.mem)))
elif '@newlines' in sys.argv or '@n' in sys.argv:
    print('\n'.join(map(str, interpreter.mem)))
else:
    print(stringify(interpreter.mem))
