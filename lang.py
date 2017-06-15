code_page  = '''¡¢£¤¥¦©¬®µ½¿€ÆÇÐÑ×ØŒÞßæçðıȷñ÷øœþ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~¶'''
code_page += '''°¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ƁƇƊƑƓƘⱮƝƤƬƲȤɓƈɗƒɠɦƙɱɲƥʠɼʂƭʋȥẠḄḌẸḤỊḲḶṂṆỌṚṢṬỤṾẈỴẒȦḂĊḊĖḞĠḢİĿṀṄȮṖṘṠṪẆẊẎŻạḅḍẹḥịḳḷṃṇọṛṣṭụṿẉỵẓȧḃċḋėḟġḣŀṁṅȯṗṙṡṫẇẋẏż«»‘’“”'''
escapemap  = '''¡¢£¤¥¦©¬®µ½¿€ÆÇÐÑ×ØŒÞßæçðıȷñ÷øœþ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`a\bcdefghijklm\nopq\rs\tuvwxyz{|}~¶'''
escapemap += '''°¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ƁƇƊƑƓƘⱮƝƤƬƲȤɓƈɗƒɠɦƙɱɲƥʠɼʂƭʋȥẠḄḌẸḤỊḲḶṂṆỌṚṢṬỤṾẈỴẒȦḂĊḊĖḞĠḢİĿṀṄȮṖṘṠṪẆẊẎŻạḅḍẹḥịḳḷṃṇọṛṣṭụṿẉỵẓȧḃċḋėḟġḣŀṁṅȯṗṙṡṫẇẋẏż«»‘’“”'''

def escape(char):
    return escapemap[code_page.find(char)]

def unescape(char):
    return '\\' + code_page[escapemap.find(char)]

def unescapify(string):
    return ''.join([char if char in code_page else unescape(char) for char in string])

def baseconvert(string, base):
    if '.' in string:
        left = len(string.split('.')[0]) if base == 1 else int(string.split('.')[0], base)
        right = string.split('.')[1]
        return left + (len(right) if base == 1 else int(right, base)) / base ** len(right)
    return int(string, base)

class Token():
    def __init__(self, type, content):
        self.type = type
        self.content = content
    def __str__(self):
        return '%s@[%s]' % (self.type, unescapify(self.content))
    def __repr__(self):
        return self.__str__()

class Tokenizer():
    def __init__(self, code):
        self.code = code.strip()
        self.index = 0
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
            return self.next() if self.hasNext() else Token('EOFToken', '')
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
            return Token('StringToken', strings[0]) if len(strings) == 1 else Token('ListToken', [Token('StringToken', string) for string in strings])
        elif self.current() == '”':
            self.advance()
            if self.current() == '\\':
                self.advance()
                return Token('StringToken', escape(self.code[self.advance()]))
            else:
                self.advance()
                return Token('StringToken', self.current())
        elif self.current() in '0123456789.':
            decimal = self.current() == '.'
            base = 10
            bases = ' bq x'
            if self.code[self.advance()] == '0':
                if self.hasNext():
                    if self.current() != ' ' and self.current() in bases: base = 2 ** bases.find(self.current())
                    elif self.current() in '0123456789': base = 8
                    elif self.current() == '.': base = 10
                else: return Token('NumberToken', 0)
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
            return Token('NumberToken', baseconvert(number, base))
        elif self.current() == '[':
            array = []
            self.advance()
            while self.hasNext() and self.current() != ']':
                array.append(self.next())
            self.advance()
            return Token('ListToken', array)
        elif self.current() == 'Þ':
            array = []
            self.advance()
            while self.hasNext() and self.current() != '»':
                array.append(self.next())
            self.advance()
            return Token('SortToken', array)
        return Token('InstructionToken', self.code[self.advance()])

instruction_queue = []
value_stack = []

code = input()

tokenizer = Tokenizer(code)
while tokenizer.hasNext():
    token = tokenizer.next()
    instruction_queue.append(token)
print(instruction_queue)
