from core import *
import arities, functions

code_page  = '''¡¢£¤¥¦©¬®µ½¿€ÆÇÐÑ×ØŒÞßæçðıȷñ÷øœþ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~¶'''
code_page += '''°¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ƁƇƊƑƓƘⱮƝƤƬƲȤɓƈɗƒɠɦƙɱɲƥʠɼʂƭʋȥẠḄḌẸḤỊḲḶṂṆỌṚṢṬỤṾẈỴẒȦḂĊḊĖḞĠḢİĿṀṄȮṖṘṠṪẆẊẎŻạḅḍẹḥịḳḷṃṇọṛṣṭụṿẉỵẓȧḃċḋėḟġḣŀṁṅȯṗṙṡṫẇẋẏż«»‘’“”'''
escapemap  = '''¡¢£¤¥¦©¬®µ½¿€ÆÇÐÑ×ØŒÞßæçðıȷñ÷øœþ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`a\bcdefghijklm\nopq\rs\tuvwxyz{|}~¶'''
escapemap += '''°¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ƁƇƊƑƓƘⱮƝƤƬƲȤɓƈɗƒɠɦƙɱɲƥʠɼʂƭʋȥẠḄḌẸḤỊḲḶṂṆỌṚṢṬỤṾẈỴẒȦḂĊḊĖḞĠḢİĿṀṄȮṖṘṠṪẆẊẎŻạḅḍẹḥịḳḷṃṇọṛṣṭụṿẉỵẓȧḃċḋėḟġḣŀṁṅȯṗṙṡṫẇẋẏż«»‘’“”'''

codeblock_tokens = {
    'ß': 'BlockSortToken',
    '€': 'BlockMapToken',
    'þ': 'BlockFilterToken',
    'ʠ': 'BlockFilterOutToken',
    '/': 'BlockReduceToken'
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
    def isList(self):
        return self.type.startswith('List')
    def isBlock(self):
        return self.type.startswith('Block')
    def isInstruction(self):
        return self.type.startswith('Instruction')
    def isCombo(self):
        return self.type.startswith('Combo')

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
    def next(self):
        if self.current() == ' ':
            self.advance()
            self.tokens.append(self.next() if self.hasNext() else Token('EOFToken', ''))
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
            self.tokens.append(Token('LiteralStringToken', strings[0]) if len(strings) == 1 else Token('ListToken', [Token('LiteralStringToken', string) for string in strings]))
        elif self.current() == '”':
            self.advance()
            if self.current() == '\\':
                self.advance()
                self.tokens.append(Token('LiteralStringToken', escape(self.code[self.advance()])))
            else:
                self.advance()
                self.tokens.append(Token('LiteralStringToken', self.current()))
        elif self.current() in '0123456789.':
            decimal = False
            base = 10
            bases = ' bq x'
            if self.code[self.advance()] == '0':
                if self.hasNext():
                    if self.current() != ' ' and self.current() in bases: base = 2 ** bases.find(self.current())
                    elif self.current() in '0123456789': base = 8
                    elif self.current() == '.': base = 10
                else:
                    self.tokens.append(Token('LiteralNumberToken', 0))
            number = ''
            if base == 10:
                self.index -= 1
            elif base != 8:
                self.advance()
            while self.hasNext():
                if self.current() in '0123456789' or self.current() == '.' and not decimal:
                    if self.current() == '.': decimal = True
                    number += self.current()
                    self.advance()
                else:
                    break
            self.tokens.append(Token('LiteralNumberToken', baseconvert(number, base)))
        elif self.current() == '[':
            array = []
            self.advance()
            while self.hasNext() and self.current() != ']':
                array.append(self.next())
            self.advance()
            self.tokens.append(Token('ListToken', array))
        elif self.current() in codeblock_tokens:
            self.advance()
            self.tokens.append(Token(codeblock_tokens[self.current()], ''))
        elif self.current() == '»':
            tokenlist = []
            buffer = 0
            while buffer or not self.tokens[-1].isBlock():
                debug('( Token Grouper found token %s )' % str(self.tokens[-1]))
                tokenlist = [self.tokens[-1]] + tokenlist
                self.tokens = self.tokens[:-1]
                debug('( Token list is now %s )' % str(self.tokens))
                if tokenlist[0].isCombo():
                    buffer += 1
                elif tokenlist[0].isBlock():
                    buffer -= 1
            self.tokens.append(Token('ComboToken', tokenlist))
        self.tokens.append(Token('InstructionToken', self.code[self.advance()]))

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
        if type(value) == type(splat([])):
            self.mem = list(value.array) + self.mem
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
            token = self.instruction_queue[0]
            arity = arities.arities[token.content]
            if len(self.mem) >= arity:
                debug('( %s operates with enough items on stack after push )' % str(token))
                function = functions.functions[token.content]
                arguments = self.popCount(arity)
                self.push(function(*arguments))
                self.instruction_queue = self.instruction_queue[1:]
                self.update()
    def next(self):
        debug('Tokens Left: %s' % str(self.tokens))
        token = self.tokens[0]
        debug('Evaluating %s' % str(token))
        self.tokens = self.tokens[1:]
        if token.isLiteral():
            debug('( Literal token )')
            self.push(token.content)
            self.update()
        elif token.isList():
            debug('( List token )')
            tokenlist = token.content
            valuelist = Interpreter.operate(tokenlist, [])
            self.push(valuelist)
            self.update
        elif token.isInstruction() and all(char in code_page for char in token.content):
            debug('( Instruction Token )')
            arity = arities.arities[token.content]
            debug('( Arity %d )' % arity)
            if arity == -1:
                debug('( Operates over entire stack )')
                function = functions.functions[token.content]
                arguments = self.popAll()
                self.push(function(*arguments))
                self.update()
            elif arity == -2:
                debug('( Operates over list )')
                function = functions.functions[token.content]
                if hasattr(self.peek(), '__iter__'):
                    self.push(function(self.pop()))
                    self.update()
                else:
                    self.push(function(*self.popAll()))
                    self.update()
            elif len(self.mem) >= arity:
                debug('( Enough items on stack )')
                function = functions.functions[token.content]
                arguments = self.popCount(arity)
                self.push(function(*arguments))
                self.update()
            else:
                debug('( Not enough items on stack; adding to queue )')
                self.instruction_queue.append(token)
        elif token.isBlock():
            listmode = type(self.peek()) == type([])
            array = self.pop() if listmode else self.popAll()
            def push(array):
                if listmode: self.push(array)
                else: self.pushAll(*array)
            if token.type == 'BlockSortToken':
                push(sorted(array, key = lambda x: Interpreter.operate([self.nextToken()], [x])))
            elif token.type == 'BlockMapToken':
                push(map(lambda x: Interpreter.operate([self.nextToken()], [x])[0], array))
            elif token.type == 'BlockFilterToken':
                push(filter(lambda x: Interpreter.operate([self.nextToken()], [x])[0], array))
            elif token.type == 'BlockFilterOutToken':
                push(filter(lambda x: not Interpreter.operate([self.nextToken()], [x])[0], array))
            elif token.type == 'BlockReduceToken':
                f = lambda x, y: Interpreter.operate([self.nextToken()], [x, y])[0]
                while len(array) > 1:
                    array[1] = f(array[0], array[1])
                    array = array[1:]
                push(array)
            self.tokens = self.tokens[1:]
            self.update()
        elif token.isCombo():
            self.mem = Interpreter.operate(token.content, self.mem)
            self.update()

verbose = True

code = input()
tokens = Tokenizer.tokenize(code)
debug('TOKENS: %s' % str(tokens))

interpreter = Interpreter(tokens)
while interpreter.hasNext():
    interpreter.next()
print('Memory:', interpreter.mem)
print('Instruction Queue:', interpreter.instruction_queue)
