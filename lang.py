code_page  = '''¡¢£¤¥¦©¬®µ½¿€ÆÇÐÑ×ØŒÞßæçðıȷñ÷øœþ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~¶'''
code_page += '''°¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ƁƇƊƑƓƘⱮƝƤƬƲȤɓƈɗƒɠɦƙɱɲƥʠɼʂƭʋȥẠḄḌẸḤỊḲḶṂṆỌṚṢṬỤṾẈỴẒȦḂĊḊĖḞĠḢİĿṀṄȮṖṘṠṪẆẊẎŻạḅḍẹḥịḳḷṃṇọṛṣṭụṿẉỵẓȧḃċḋėḟġḣŀṁṅȯṗṙṡṫẇẋẏż«»‘’“”'''

'''

Command List / Escape List

¡
¢
£
¤
¥
¦
©
¬
®
µ
½¿
€
Æ
Ç
Ð
Ñ
× Construct a rectangle of width <left> and height <right> with character <third>
Ø
Œ
Þ
ß
æ
ç
ð
ı
ȷ
ñ
÷
ø
œ
þ

!
"
#
$
%
&
'
(
)
*
+
,
-
.
/
0
1
2
3
4
5
6
7
8
9
:
;
<
=
>
?
@
A
B
C
D
E
F
G
H
I
J
K
L
M
N
O
P
Q
R
S
T
U
V
W
X
Y
Z
[
\
]
^
_
`
a
b
c
d
e
f
g
h
i
j
k
l
m
n
o
p
q
r
s
t
u
v
w
x
y
z
{
|
}
~
¶
°
¹
²
³
⁴
⁵
⁶
⁷
⁸
⁹
⁺
⁻
⁼
⁽
⁾
Ɓ
Ƈ
Ɗ
Ƒ
Ɠ
Ƙ
Ɱ
Ɲ
Ƥ
Ƭ
Ʋ
Ȥ
ɓ
ƈ
ɗ
ƒ
ɠ
ɦ
ƙ
ɱ
ɲ
ƥ
ʠ
ɼ
ʂ
ƭ
ʋ
ȥ
Ạ
Ḅ
Ḍ
Ẹ
Ḥ
Ị
Ḳ
Ḷ
Ṃ
Ṇ
Ọ
Ṛ
Ṣ
Ṭ
Ụ
Ṿ
Ẉ
Ỵ
Ẓ
Ȧ
Ḃ
Ċ
Ḋ
Ė
Ḟ
Ġ
Ḣ
İ
Ŀ
Ṁ
Ṅ
Ȯ
Ṗ
Ṙ
Ṡ
Ṫ
Ẇ
Ẋ
Ẏ
Ż
ạ
ḅ
ḍ
ẹ
ḥ
ị
ḳ
ḷ
ṃ
ṇ
ọ
ṛ
ṣ
ṭ
ụ
ṿ
ẉ
ỵ
ẓ
ȧ
ḃ
ċ
ḋ
ė
ḟ
ġ
ḣ
ŀ
ṁ
ṅ
ȯ
ṗ
ṙ
ṡ
ṫ
ẇ
ẋ
ẏ
ż
«
»
‘
’
“
”

'''


def encodeBinary(string, sep = ''):
    string = string.replace('\n', '¶')
    binary = ''
    for char in string:
        sub = bin(code_page.index(char))[2:]
        binary += '0' * (8 - len(sub)) + sub
    return binary

def encodeHex(string, sep = ''):
    string = string.replace('\n', '¶')
    hexadecimal = ''
    for char in string:
        sub = hex(code_page.index(char))[2:]
        hexadecimal += '0' * (2 - len(sub)) + sub
    return hexadecimal

def decodeBinary(binary, sep = ''):
    string = ''
    if sep:
        return ''.join(code_page[int(index, 2)] for index in binary.split(sep))
    for i in range(0, len(binary), 8):
        string += code_page[int(binary[i:i + 8], 2)]
    return string

def decodeHex(hexadecimal, sep = ''):
    string = ''
    if sep:
        return ''.join(code_page[int(index, 16)] for index in binary.split(sep))
    for i in range(0, len(hexadecimal), 2):
        string += code_page[int(hexadecimal[i:i + 2], 16)]
    return string

def escape(char):
    return char # TODO

def baseconvert(string, base):
    if '.' in string:
        left = len(string.split('.')[0]) if base == 1 else int(string.split('.')[0], base)
        right = string.split('.')[1]
        return left + (len(right) if base == 1 else int(right, base)) / base ** len(right)
    return int(string, base)

class Token():
    def __init__(self, type, name, content):
        self.type = type
        self.name = name
        self.content = content
    def __str__(self):
        return '%s:%s:[%s]' % (self.type, self.name, self.content)
    def __repr__(self):
        return self.__str__()

class Tokenizer():
    def __init__(self, code):
        self.code = code.strip()
        self.index = 0
    def hasNext(self):
        return self.index < len(self.code)
    def next(self):
        if self.code[self.index] == ' ':
            self.index += 1
            return self.next() if self.hasNext() else Token('EOFToken', '', '')
        elif self.code[self.index] == '\"':
            self.index += 1
            string = ''
            while self.code[self.index] != '\"':
                if self.code[self.index] != '\\':
                    string += self.code[self.index]
                else:
                    string += escape(self.code[self.index + 1])
                    self.index += 1
                self.index += 1
            self.index += 1
            return Token('StringToken', '', string)
        elif self.code[self.index] == '\'':
            self.index += 1
            if self.code[self.index] == '\\':
                self.index += 2
                return Token('StringToken', '', escape(self.code[self.index - 1]))
            else:
                self.index += 1
                return Token('StringToken', '', self.code[self.index])
        elif self.code[self.index] in '0123456789.':
            decimal = self.code[self.index] == '.'
            self.index += 1
            base = 10
            bases = ' ubtqphs n UdTQPxSONM'
            if self.code[self.index - 1] == '0':
                if self.hasNext():
                    if self.code[self.index] != ' ' and self.code[self.index] in bases: base = bases.find(self.code[self.index])
                    elif self.code[self.index] in '0123456789': base = 8
                    elif self.code[self.index] == '.': base = 10
                else: return Token('NumberToken', '', 0)
            number = ''
            if base == 10:
                self.index -= 1
            elif base != 8:
                self.index += 1
            while self.hasNext():
                if self.code[self.index] in '0123456789' or self.code[self.index] == '.' and not decimal:
                    if self.code[self.index] == '.': decimal = True
                    number += self.code[self.index]
                    self.index += 1
                else:
                    break
            return Token('NumberToken', '', baseconvert(number, base))
        elif self.code[self.index] == '[':
            array = []
            self.index += 1
            while self.hasNext() and self.code[self.index] != ']':
                array.append(self.next())
            self.index += 1
            return array
        else:
            self.index += 1
            return Token('TestToken', self.code[self.index - 1], 'content')

instruction_queue = []
value_stack = []

code = input()

tokenizer = Tokenizer(code)
while tokenizer.hasNext():
    token = tokenizer.next()
    instruction_queue.append(token)
print(instruction_queue)
