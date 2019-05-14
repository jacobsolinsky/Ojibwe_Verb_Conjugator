import re
from persons import *
'''
Internal orthography correspondence
to double vowel orthography
VOWELS
a = a
A = aa
e = ε (nonpalatalizing short i)
E = e
i = i
I = ii
o = o
O = oo

v = any short vowel
V = any long vowel

CONSONANTS
m = m
b = b
p = p
w = w
n = n
d = d
t = t
N = algonquian θ (alternates between n and zh)
s = s
z = z
j = j
c = ch
Z = zh
S = sh
y = y
g = g
k = k
h = glottal stop
C = any consonant
F = any fortis consonant
L = any lenis consonant
Q = any nasal consonant
Y = any palatalizable consonant
'''
#Converting to internal orthography
C = "hbpwmdtnszSZcjykghN"
v = 'aieo'
V= 'AIEO'
F = 'ptsSck'
L = 'bdzZjg'
Q = 'nm'
Y = 'Ndtsz'

def fromdoublevowel(string):
    skip = False
    result = []
    for i, letter in enumerate(string):
        if skip:
            skip = False
        elif letter == 'e':
            result.append('E')
        elif i == len(string) - 1:
            result.append(letter)
        elif letter in 'aio' and string[i+1] == letter:
            result.append(letter.upper())
            skip = True
        elif letter in 'szc' and string[i+1] == 'h':
            result.append(letter.upper())
            skip = True
        elif letter == "'":
            result.append('h')
        else:
            result.append(letter)
    return result

def todoublevowel(string):
    result = []
    for letter in string:
        if letter in 'AIO':
            result.append(2* letter.lower())
        elif letter in 'cSZ':
            result.append(letter.lower()+'h')
        elif letter == 'e':
            result.append('i')
        elif letter == 'E':
            result.append('e')
        elif letter == 'x':
            pass
        elif letter  == 'N':
            if string[string.index(letter)-1] == 'n':
                pass
            else:
                result.append('n')
        elif letter == 'h':
            result.append("'")
        else:
            result.append(letter)
    return ''.join(result)

def replace_position(position, list1, list2):
    return list1[:position] + list2 + list1[position+1:]






#Processes
PALATALIZATIONS = {
        'N':'Z',
        'd':'j',
        't':'c',
        's':'S',
        'z':'Z',
        }
LENGTHENINGS = {
        'a':'A',
        'e':'I',
        'i':'I',
        'o':'O'
        }
SHORTENINGS = {
        'A':'a',
        'E':'i',
        'I':'i',
        'O':'o'
        }
FORTIFICATIONS = {
        'b':'p',
        'd':'t',
        'z':'s',
        'j':'c',
        'Z':'S',
        'g':'k'
        }
LENITIONS = {v: k for k, v in FORTIFICATIONS.items()}
INITIALVOWELCHANGES = {
        'a':'E',
        'e':'E',
        'i':'E',
        'o':'wE',
        'A':'ayA',
        'I':'A',
        'E':'ayE',
        'O':'wA'
        }
class Morpheme():
    def __init__(self, form):
        self.form = fromdoublevowel(form)
        self.stem = False
        self.modal = False
        self.peripheral = False
        self.null = False
    def __repr__(self):
        return todoublevowel(self.form)
    def prep(self,  verb):
        self.verb = verb
        self.position = verb.morphemelist.index(self)
        if self.position == len(self.verb.morphemelist) -1:
            self.preceding = self.verb.morphemelist[self.position-1]
            self.ps = ''
            for morpheme in self.verb.morphemelist[:self.position]:
                self.ps = self.ps+''.join(morpheme.form)
            self.following = Nullmorpheme()
            self.fs = ''
        elif self.position == 0:
            self.following = self.verb.morphemelist[self.position+1]
            self.fs = ''.join(self.following.form)
            self.preceding = Nullmorpheme()
            self.ps = ''
        else:
            self.preceding = self.verb.morphemelist[self.position-1]
            self.ps = ''
            for morpheme in self.verb.morphemelist[:self.position]:
                self.ps = self.ps+''.join(morpheme.form)
            self.following = self.verb.morphemelist[self.position+1]
            self.fs = ''.join(self.following.form)

    def mutate(self):
        if re.search(f'$[{C}]', self.ps):
                i_epenthesis(self.preceding)
class Nullmorpheme(Morpheme):
    def __init__(self):
        super().__init__('')
        self.null = True
#PERSONAL SUFFIXES
class Ni(Morpheme):
    def __init__(self):
        super().__init__('ni')
    def mutate(self):
        if re.search('^b', self.fs):
            self.form = list('im')
        elif re.search(f'^[{L}]', self.fs):
            self.form = list('in')
        elif re.search(f'^[{v}AE]', self.fs):
            self.form = list('ind')
            if re.search('^o', self.fs):
                initial_vowel_lengthen(self.following)
        elif re.search('^[OI]', self.fs):
            self.form = list('n')

class Gi(Morpheme):
    def __init__(self):
        super().__init__('gi')
    def mutate(self):
        if re.search(f'^[{v}AE]', self.fs):
            self.form = list('gid')
            if re.search('^o', self.fs):
                initial_vowel_lengthen(self.following)
        elif re.search('^[OI]', self.fs):
            self.form = list('g')

class O(Morpheme):
    def __init__(self):
        super().__init__('o')
    def mutate(self):
        if re.search(f'^[{v}AE]', self.fs):
            self.form = list('od')
            if re.search('^o', self.fs):
                initial_vowel_lengthen(self.following)
        elif re.search('^I', self.fs):
            self.form = ['w']
        elif re.search('^O', self.fs):
            self.form = []
#Stem class:
class Stem(Morpheme):
    def __init__(self, string):
        super().__init__(string)
        self.stem = True

#THEME SIGNS 1
class M(Morpheme):
    def __init__(self):
        super().__init__('m')
    def mutate(self):
        e_epenthesis(self.preceding)

class I(Morpheme):
    def __init__(self):
        super().__init__('')
    def mutate(self):
        i_epenthesis(self.preceding)
        self.form.append(self.preceding.form.pop())
        if self.following.peripheral:
            self.verb.morphemelist.remove(self.following)
        if self.following.modal:
            self.form.extend(list('nA'))
        if type(self.following) == Nimperative:
            self.verb.morphemelist.remove(self.following)
        elif type(self.following) == Og:
            self.following.form == ['k']
class Am(Morpheme):
    def __init__(self):
        super().__init__('am')
    def mutate(self):
        if type(self.following) == Ni_animate:
            pass
        elif type(self.following) == Nimperative:
            self.form = ['a']
        elif re.search(f'^[{Q}]', self.fs):
            self.form = ['A']
#THEME SIGNS 2
class Aa(Morpheme):
    def __init__(self):
        super().__init__('aa')
    def mutate(self):
        if type(self.following) == Ind:
            self.form = []
class N1stperson(Morpheme):
    def __init__(self):
        super().__init__('n')
    def mutate(self):
        #AW Contraction
        if re.search('aw$', self.ps):
            self.preceding.form.pop()
            self.preceding.form[-1] = 'O'
        else:
            e_epenthesis(self.preceding)
        if type(self.following) in [K2ndperson, Si]:
            self.form.pop()
        if type(self.following) == Mw:
            self.form.extend(list('in'))
class Go(Morpheme):
    def __init__(self):
        super().__init__('go')
    def mutate(self):
        #AW Contraction
        if re.search('aw$', self.ps):
            self.preceding.form.pop()
            self.preceding.form[-1] = 'A'
        elif self.preceding.form == list('iN'):
            self.preceding.form == ['']
        else:
            e_epenthesis(self.preceding)
        if self.following.peripheral:
            self.form[-1] = 'O'
        if not self.following:
            self.form.pop()
class Goo(Morpheme):
    def __init__(self):
        super().__init__('goo')
    def mutate(self):
        #AW Contraction
        if re.search('aw$', self.ps):
            self.preceding.form.pop()
            self.preceding.form[-1] = 'A'
        elif self.preceding.form == list('iN'):
            self.preceding.form == ['']
        else:
            e_epenthesis(self.preceding)
class Shi(Morpheme):
    def __init__(self):
        super().__init__('shi')
    def mutate(self):
        if self.following.null or type(self.following) == Aam:
            self.form = list('Sin')
#Negative
class Si(Morpheme):
    def __init__(self):
        super().__init__('si')
    def mutate(self):
        if re.search(f'[{Q}]$', self.ps):
            self.preceding.form[-1] = 'n'
            initial_lenite(self)

class Sin(Morpheme):
    def __init__(self):
        super().__init__('sin')
    def mutate(self):
        if re.search(f'[{Q}]$', self.ps):
            self.preceding.form[-1] = 'n'
            initial_lenite(self)
        elif re.search(f'd$', self.ps):
            self.preceding.form.pop()
class Wnegative(Morpheme):
    def __init__(self):
        super().__init__('w')
    def mutate(self):
            if type(self.following) == Ng:
                if self.verb.dubitative:
                    return
                else:
                    self.form = []
                    return
            if re.search(f'[{C}]$', self.ps):
                o_epenthesis(self.preceding)
            if type(self.preceding) == Ni_inanimate:
                self.form = []
            elif self.following.peripheral:
                final_vowel_lengthen(self.preceding)
                self.form = []
            elif type(self.following) == D and self.fs == 'd' or type(self.following) == G:
                self.following.form = list('gw')
                self.form = []
            elif type(self.following) == K2ndperson:
                self.form = []
            elif re.search(f'^[{C}]', self.fs):
                final_vowel_lengthen(self.preceding)
                self.form = []
class Nnegativeaugment(Morpheme):
    def __init__(self):
        super().__init__('n')
class Wdelayed(Morpheme):
    def __init__(self):
        super().__init__('w')
    def mutate(self):
        o_epenthesis(self.preceding)
        if re.search(self.fs, f'^[{C}]'):
            final_vowel_lengthen(self.preceding)
            self.form = []
class Wdubitative(Morpheme):
    def __init__(self):
        super().__init__('w')
    def mutate(self):
        o_epenthesis(self.preceding)
        if type(self.following) == Ng:
            if self.verb.dubitative:
                return
        if type(self.following) == D and self.fs == 'd' or type(self.following) == G:
            self.following.form = list('gw')
            self.form = []
        elif re.search(f'^[{C}]', self.fs):
            if not self.preceding.stem:
                final_vowel_lengthen(self.preceding)
            self.form = []

#CENTRAL SIGNS
class Mw(Morpheme):
    def __init__(self):
        super().__init__('mw')
    def mutate(self):
        e_epenthesis(self.preceding)
        if self.following.peripheral:
            self.verb.morphemelist.remove(self.following)
        if self.following.modal:
            self.form.append('A')
class Min(Morpheme):
    def __init__(self):
        super().__init__('min')
    def mutate(self):
        e_epenthesis(self.preceding)
        if self.following.peripheral:
            self.verb.morphemelist.remove(self.following)
        if self.following.modal:
            self.form.append('A')

class Local_singular(Morpheme):
    def __init__(self):
        super().__init__('')
    def mutate(self):
        if self.following.modal:
            self.form = list('nA')
        if self.form == list('nA'):
            if type(self.preceding) == Wnegative:
                self.preceding.form = []
                final_vowel_lengthen(self.preceding.preceding)
            else:
                e_epenthesis(self.preceding)

class Nsingular(Morpheme):
    def __init__(self):
        super().__init__('n')
    def mutate(self):
        if self.following.modal:
            self.form.append('A')

class Naan(Morpheme):
    def __init__(self):
        super().__init__('naan')
    def mutate(self):
        if self.following.modal:
            self.form.pop()
        if self.following.peripheral:
            self.form.append('i')

class Daa(Morpheme):
    def __init__(self):
        super().__init__('daa')
    def mutate(self):
        if self.following.peripheral:
            self.form += list('ni')
        if re.search('m$', self.ps):
            self.preceding.form[-1] = 'n'

class Naawaa(Morpheme):
    def __init__(self):
        super().__init__('naawaa')
class W3rdperson(Morpheme):
    def __init__(self):
        super().__init__('w')
    def mutate(self):
        if self.following.null:
            self.form = ['x']
            return
        if not self.following.peripheral:
            o_epenthesis(self.preceding)
        if type(self.following) == Dog:
            if (not self.verb.subj.animacy) and self.verb.obj is None and (type(self.preceding) in [Sin, Stem]) or\
            (type(self.preceding) == Wnegative and type(self.following == Dog) and type(self.preceding.preceding) == Si):
                self.form = []
            else:
                self.form = list('wi')
        elif re.search(f'^[{C}]', self.fs):
            final_vowel_lengthen(self.preceding)
            self.form = []

#Conjunct Indexing Morphemes
class Aan(Morpheme):
    def __init__(self):
        super().__init__('aan')
    def mutate(self):
        if re.search(f'[{v+V}]$', self.ps):
            self.preceding.form.append('y')
        if type(self.following) == Ban:
            self.form[-1] = 'm'
            initial_vowel_lengthen(self.following)
        if self.following.peripheral:
            i_epenthesis(self)
class Ag(Morpheme):
    def __init__(self):
        super().__init__('ag')
    def mutate(self):
        if type(self.preceding) == Aa:
            self.preceding.form = []
            return
        if self.following.peripheral:
            i_epenthesis(self)
class An(Morpheme):
    def __init__(self):
        super().__init__('an')
    def mutate(self):
        if re.search(f'[{v+V}]$', self.ps):
            self.preceding.form.append('y')
        if type(self.following) == Ban:
            self.form[-1] = 'm'
        if self.following.peripheral:
            i_epenthesis(self)
class Ad(Morpheme):
    def __init__(self):
        super().__init__('ad')
    def mutate(self):
        if type(self.preceding) == Aa:
            self.preceding.form = []
            return
        if self.following.peripheral:
            i_epenthesis(self)
class Aang(Morpheme):
    def __init__(self):
        super().__init__('aang')
    def mutate(self):
        if re.search(f'[{v+V}]$', self.ps):
            self.preceding.form.append('y')
        if self.following.peripheral:
            i_epenthesis(self)
class Angid(Morpheme):
    def __init__(self):
        super().__init__('angid')
    def mutate(self):
        if type(self.preceding) == Aa:
            self.preceding.form = []
        elif re.search(f'[{v+V}]$', self.ps):
            self.preceding.form.append('y')
        if self.following.peripheral:
            i_epenthesis(self)
class Ang(Morpheme):
    def __init__(self):
        super().__init__('ang')
    def mutate(self):
        if type(self.preceding) == Aa:
            self.preceding.form = []
        elif re.search(f'[{v+V}]$', self.ps):
            self.preceding.form.append('y')
        if self.following.peripheral:
            i_epenthesis(self)
class Egw(Morpheme):
    def __init__(self):
        super().__init__('egw')
    def mutate(self):
        if type(self.preceding) == Aa:
            self.preceding.form = []
        elif re.search(f'[{v+V}]$', self.ps):
            self.preceding.form.append('y')
        if type(self.following) == Ban:
            self.form[-1] = 'i'
        if self.following.peripheral:
            self.form[-1] = 'i'
class Ng(Morpheme):
    def __init__(self):
        super().__init__('ng')
    def mutate(self):
        if self.verb.dubitative:
            self.form = list('Ing')
        if self.form == list('ng'):
            i_epenthesis(self.preceding)

class Ind(Morpheme):
    def __init__(self):
        super().__init__('ind')
    def Mutate(self):
        if self.following.peripheral:
            i_epenthesis(self)

class Agogw(Morpheme):
    def __init__(self):
        super().__init__('agogw')
    def mutate(self):
        if self.following.modal:
            self.form = list('agOgw')
class D(Morpheme):
    def __init__(self):
        super().__init__('d')
    def mutate(self):
        if self.verb.dubitative:
            self.form = list('gw')
        if self.form == list('gw'):
            o_epenthesis(self.preceding)
        elif re.search(f'[{Q}]$', self.ps):
            self.preceding.form[-1] = 'n'
            self.form = ['g']
        elif type(self.following) == Ban:
            self.following.form[0] = 'p'
            self.form = []
        if self.following.peripheral:
            i_epenthesis(self)
class G(Morpheme):
    def __init__(self):
        super().__init__('g')
    def mutate(self):
        if self.form == list('gw'):
            o_epenthesis(self.preceding)
        elif self.ps[-1] == 'd':
            self.preceding.form.pop()
            self.form = ['k']
        if type(self.following) == Ban:
            i_epenthesis(self)
class K2ndperson(Morpheme):
    def __init__(self):
        super().__init__('k')
class Waaw(Morpheme):
    def __init__(self):
        super().__init__('waaw')
    def mutate(self):
        if re.search(f'[{C}]w$', self.ps):
            self.preceding.form.pop()
        if re.search(f'^[{C}]', self.fs) or self.following.peripheral or \
        type(self.following) == Nullmorpheme:
            self.form.pop()
class Waa(Morpheme):
    def __init__(self):
        super().__init__('waa')
    def mutate(self):
        o_epenthesis(self.preceding)
class Ni_animate(Morpheme):
    def __init__(self):
        super().__init__('ni')
    def mutate(self):
        if re.search(f'[{C}]$', self.ps):
            e_epenthesis(self.preceding)
        if self.following.modal:
            self.form[-1] = 'A'
        if self.following.peripheral:
            self.verb.morphemelist.remove(self.following)
            self.following = Nullmorpheme()
        if self.following.null:
            self.form.append('x')
class Ni_inanimate(Morpheme):
    def __init__(self):
        super().__init__('ni')
    def mutate(self):
        if re.search(f'[{C}]$', self.ps):
            e_epenthesis(self.preceding)
        if self.following.null:
            self.form.append('x')


class Kdelayed(Morpheme):
    def __init__(self):
        super().__init__('k')
    def mutate(self):
        if re.search(f'[{Q}]$', self.ps):
            self.preceding.form[-1] = 'n'
            initial_lenite(self)

class Ke(Morpheme):
    def __init__(self):
        super().__init__('ke')
    def mutate(self):
        if re.search(f'[{Q}]$', self.ps):
            self.preceding.form[-1] = 'n'
            initial_lenite(self)
        if re.search(f'^[{V}]', ''.join(self.following.form)):
            self.form.pop()
class En(Morpheme):
    def __init__(self):
        super().__init__('en')
    def mutate(self):
        if type(self.preceding) == Og:
            self.form[0] = 'o'
class Aam(Morpheme):
    def __init__(self):
        super().__init__('aang')

class Ban(Morpheme):
    def __init__(self):
        super().__init__('ban')
        self.modal = True
    def mutate(self):
        if not re.search('m$', self.ps):
            e_epenthesis(self.preceding)
        if self.following.peripheral:
            self.form.append('E')
class Dog(Morpheme):
    def __init__(self):
        super().__init__('dog')
        self.modal = True
    def mutate(self):
        if self.verb.conjunct:
            self.form = list('En')
            if type(self.preceding) == Waaw:
                self.preceding.form += 'w'
        if self.following.peripheral:
            if self.form == list('dog'):
                self.form.extend(list('En'))


class An_(Morpheme):
    def __init__(self):
        super().__init__('an')
        self.peripheral = True
    def mutate(self):
        if re.search(f'[{C}]w$',self.ps):
            self.preceding.form[-1] = 'O'
            self.form = self.form[-1:]
        if re.search(f'[{v+V}]$', self.ps):
            self.form = self.form[-1:]
class Ag_(Morpheme):
    def __init__(self):
        super().__init__('ag')
        self.peripheral = True
    def mutate(self):
        if re.search(f'[{C}]w$',self.ps):
            self.preceding.form[-1] = 'O'
            self.form = self.form[-1:]
        if re.search(f'[{v+V}]$', self.ps):
            self.form = self.form[-1:]

class Ah_(Morpheme):
    def __init__(self):
        super().__init__("a'")
        self.peripheral = True
    def mutate(self):
        if re.search(f'[{C}]w$',self.ps):
            self.preceding.form[-1] = 'O'
            self.form = self.form[-1:]
        if re.search(f'[{v+V}]$', self.ps):
            self.form = self.form[-1:]

class Nimperative(Morpheme):
        def __init__(self):
            super().__init__('n')
        def mutate(self):
            if re.search(f'[{Q}]$', self.ps):
                e_epenthesis(self.preceding)
            if self.following.peripheral:
                self.verb.morphemelist.remove(self.following)
class Og(Morpheme):
    def __init__(self):
            super().__init__('g')
    def mutate(self):
        if self.verb.type == 'vta' and self.verb.mode == 'neutral':
            e_epenthesis(self.preceding)
            self.form = ['k']
        else:
            o_epenthesis(self.preceding)
        if self.following.peripheral:
            self.verb.morphemelist.remove(self.following)




#Morpheme Sets
def INDEPENDENTCENTRALI(person):
        if person.locality:
            if person.name in ['p1','p2']:
                return Local_singular()
            if person.person == 1:
                return Min()
            else:
                return Mw()
        elif person.person in [3,0]:
            return W3rdperson()
        elif person.person == 'X':
            return Mw()
def INDEPENDENTCENTRALII(person):
        if person.person == 'X':
            return Mw()
        if not person.plurality:
            return Nsingular()
        elif person.person == 1:
            return Min()
        elif person.plurality:
            return Naawaa()

def INDEPENDENTCENTRALIII(person):
    person = person.name
    d = {'p1p': Naan(),
         'p21': Naan(),
         'p2p':Waaw(),
         'p3p': Waaw()}
    return d[person]
def INDEPENDENTCENTRALI_(primary):
    if primary == p1p:
        return Min()
    elif primary == p2p:
        return Mw()
    else:
        return Local_singular()
def CONJUNCTCENTRALI(person):
    person = person.name
    conjunctcentrali = {
         'p1':Aan(),
         'p2':An(),
         'p1p':Aang(),
         'p21':Ang(),
         'p2p':Egw(),
         'pX':Ng(),
         'p3':D(),
         'p3p':D(),
         'p3o':D(),
         'p3op':D()
            }
    return conjunctcentrali[person]


def CONJUNCTCENTRALII(person):
    person = person.name
    conjunctcentralii = {'p1':Ag(),
         'p2':Ad(),
         'p1p':Angid(),
         'p21':Ang(),
         'p2p':Egw(),
         'pX':Ind()}
    return conjunctcentralii[person]
def CONJUNCTCENTRALIII(primary):
    person = primary.name
    conjunctcentraliii = {'p1p':Aang(),
                          'p2':An(),
                          'p2p':Egw()
            }
    return conjunctcentraliii[person]
def CONJUNCTCENTRALIV(primary):
    if primary == p2:
        return Aan()
    elif primary == p2p:
        return Agogw()
def PRIMACY(person):
    person = person.name
    primacy = {'p0o':0,
         'p0op':0,
         'p0':1,
         'p0p':1,
         'p3o':2,
         'p3op':2,
         'p3':3,
         'p3p':3,
         'pX':4,
         'p1':5,
         'p1p':7,
         'p2':6,
         'p21':6,
         'p2p':6}
    return primacy[person]
PERIPHERALS = {
        p3: Nullmorpheme(),
        p3p: Ag_(),
        p3o: An_(),
        p3op: Ah_()}




#Palatalizes final consonant of morpheme
def final_palatalize(morpheme):
    if re.search(f'[{Y}]$', ''.join(morpheme.form)):
        morpheme.form[-1] = PALATALIZATIONS[morpheme.form[-1]]

#Fortifies initial consonant of morpheme
def initial_fortify(morpheme):
    if re.search(f'^[{L}]', ''.join(morpheme.form)):
        morpheme.form[0] = FORTIFICATIONS[morpheme.form[0]]

#Lenites initial consonant of morpheme
def initial_lenite(morpheme):
    if re.search(f'^[{F}]', ''.join(morpheme.form)):
        morpheme.form[0] = LENITIONS[morpheme.form[0]]
def initial_vowel_change(morpheme):
    position = re.search(f'^[{C}]*[{v+V}]', ''.join(morpheme.form)).end() - 1
    morpheme.form = replace_position(position, morpheme.form, list(INITIALVOWELCHANGES[morpheme.form[position]]))

def initial_vowel_lengthen(morpheme):
    position = re.search(f'^[{C}]*[{v+V}]', ''.join(morpheme.form)).end() - 1
    morpheme.form[position] = LENGTHENINGS[morpheme.form[position]]
def final_vowel_lengthen(morpheme):
    mf = ''.join(morpheme.form)
    if re.search(f'[{v}]$', mf):
        morpheme.form[-1] = LENGTHENINGS[morpheme.form[-1]]
#Appends an o to the end of a morpheme
def o_epenthesis(morpheme):
    mf = ''.join(morpheme.form)
    if re.search(f'[{C}]$', mf):
        morpheme.form += 'o'

#Appends an ε to the end of a morpheme
def e_epenthesis(morpheme):
    mf = ''.join(morpheme.form)
    if re.search(f'[{C}]w$', mf):
        morpheme.form[-1] = 'o'
    elif re.search(f'[{C}]$', mf):
        morpheme.form += 'e'

#Appends an i to the end of a morpheme and palatalizes self.preceding consonant, if possible
def i_epenthesis(morpheme):
    mf = ''.join(morpheme.form)
    if re.search(f'[{C}]w$',mf):
        morpheme.form[-1] = 'o'
    elif re.search(f'[{C}]$', mf):
       final_palatalize(morpheme)
       morpheme.form += 'i'
#These are the only
def apocope(morpheme):
    mf = ''.join(morpheme.form)
    if re.search(f'[{V}]', mf) or len(re.findall(f'[{v}]', mf)) >2:
        if re.search(f'[{v}]$', mf):
            morpheme.form.pop()
def final_w_loss(morpheme):
    if re.search(f'[{C}]w$', ''.join(morpheme.form)):
        morpheme.form.pop()
