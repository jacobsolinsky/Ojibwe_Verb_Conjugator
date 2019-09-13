class Person:
    def __init__(self, person, plurality, animacy, locality, obviacy, name):
        self.person  = person
        self.plurality = plurality
        self.animacy = animacy
        self.locality = locality
        self.obviacy = obviacy
        self.name = name
class Person21:
    def __init__(self):
        pass
    def __eq__(self, b):
        if b in [1, 2, 21]:
            return True
        else:
            return False
    
p1 = Person(person = 1,
            plurality = False,
            animacy = True,
            locality = True,
            obviacy = False,
            name = 'p1')
p1p = Person(person = 1,
            plurality = True,
            animacy = True,
            locality = True,
            obviacy = False,
            name = 'p1p') 
p21 = Person(person = Person21(),
            plurality = True,
            animacy = True,
            locality = True,
            obviacy = False,
            name = 'p21')
p2 = Person(person = 2,
            plurality = False,
            animacy = True,
            locality = True,
            obviacy = False,
            name = 'p2')
p2p = Person(person = 2,
            plurality = True,
            animacy = True,
            locality = True,
            obviacy = False,
            name = 'p2p')
p3 = Person(person = 3,
            plurality = False,
            animacy = True,
            locality = False,
            obviacy = False,
            name = 'p3')
p3o = Person(person = 3,
            plurality = False,
            animacy = True,
            locality = False,
            obviacy = True,
            name = 'p3o')
p3op = Person(person = 3,
            plurality = True,
            animacy = True,
            locality = False,
            obviacy = True,
            name = 'p3o')
p3p = Person(person = 3,
            plurality = True,
            animacy = True,
            locality = False,
            obviacy = False,
            name = 'p3p')
p0 = Person(person = 0,
            plurality = False,
            animacy = False,
            locality = False,
            obviacy = False,
            name = 'p0')
p0p = Person(person = 0,
            plurality = True,
            animacy = False,
            locality = False,
            obviacy = False,
            name = 'p0p')
p0o = Person(person = 0,
            plurality = False,
            animacy = False,
            locality = False,
            obviacy = True,
            name = 'p0o')
p0op = Person(person = 1,
            plurality = True,
            animacy = False,
            locality = False,
            obviacy = True,
            name = 'p0op')
pX = Person(person = None,
            plurality = False,
            animacy = True,
            locality = True,
            obviacy = False, 
            name = 'pX')
TOPERSON = {'1':p1,
            '1p':p1p,
            '21':p21,
            '2':p2,
            '2p':p2p,
            '3':p3,
            '3p':p3p,
            "3'":p3o,
            "3'p":p3op,
            '0':p0,
            '0p':p0p,
            "0'":p0o,
            "0'p":p0op,
            'X':pX
        }
    