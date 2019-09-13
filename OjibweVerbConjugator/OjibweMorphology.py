#%%
import sys
from morphemes import *
from persons import *
import re
VAI = 1
VII = 2
VTI = 3
VTA = 4
VAIO = 5
VAI2 = 6
VTI2 = 7


class Verb:
    def __init__(self, lemma, subj, obj = None, order = 'independent', mode = 'neutral', polarity = 'True', focus = None, type = None):
        self.subj = TOPERSON.get(subj)
        self.obj = TOPERSON.get(obj)
        self.order = order
        self.mode = mode
        self.focus = focus
        if self.focus == 'actor':
            self.focus = self.subj
        elif self.focus == 'goal':
            self.focus = self.obj
        assert self.mode in ['neutral', 'preterite', 'dubitative', 'preterite-dubitative', 'prohibitative', 'delayed'],\
        "Not a valid Mode"
        self.preterite = mode in ['preterite', 'preterite-dubitative']
        self.dubitative = mode in ['dubitative', 'preterite-dubitative']
        self.modal = mode in ['preterite', 'dubitative', 'preterite-dubitative']
        self.conjunct = order in ['conjunct', 'changedconjunct']
        self.independent = order == 'independent'
        self.imperative = order == 'imperative'
        if self.preterite and self.dubitative and self.order == 'independent':
            #This causes the verb to conjugate similar to a conjunct verb when it is independent but
            #has the preterite-dubitative mode
            self.conjunct = True
            self.order = 'conjunct'
            self.pretdub = True
        else:
            self.pretdub = False
        self.polarity = eval(polarity)
        self.lemma = Stem(lemma)
        self.morphemelist = [self.lemma]
        self.form = []
        self.type = type
        if self.obj:
            assert (self.subj.animacy or self.obj.animacy), "Subject and Object cannot both be inanimate"
            assert self.subj != self.obj, "Use Reflexive VAI for this VTA stem"
            if self.subj == p21:
                assert not self.obj in [p1, p1p, p2, p2p], \
               """Inclusive Giinawind can't act on itself or
               be acted upon by itself.
               """
            if self.obj == p21:
                assert not self.subj in [p1, p1p, p2, p2p], \
                """Inclusive Giinawind can't act on itself or
               be acted upon by itself.
               """
        if self.imperative:
            assert not (self.dubitative or self.preterite),\
            "Imperatives cannot be preterite or dubitative"
            assert self.subj.person == 2, "Imperatives cannot have non-2nd person subjects"
        else:
            assert  not self.mode in ['prohibitative', 'delayed'],\
            "Prohibitative and Delayed are imperative moods only"
        if self.order != "changedconjunct":
            assert  not self.focus, "Only participles can have focus"
        print(locals())
    def __call__(self):
        self.conjugate()
        return todoublevowel(self.form)
    def conjugate(self):
        if self.order == 'changedconjunct':
            initial_vowel_change(self.morphemelist[0])
        if not self.obj:
            if self.subj.animacy:
                self.vai_select()
            else:
                self.vii_select()
        else:
            if self.obj.animacy:
                self.vta_select()
            else:
                self.vti_select()
        self.assemble()
        return todoublevowel(self.form)
    def vai_select(self):
        if self.type is None:
            self.type = 'vai'
        if self.type == VAI2:
            self.morphemelist.append(Am())
            self.lemma.form.pop()
            self.lemma.form.pop()
        #Select person prefix
        if self.order == 'independent':
            if self.subj.person == 2:
                self.morphemelist.insert(0, Gi())
            elif self.subj.person == 1:
                self.morphemelist.insert(0, Ni())
        else:
            pass
        #Select central suffix
        if self.imperative:
            if self.mode == 'delayed':
                self.morphemelist.append(Wdelayed())
                self.morphemelist.append(Kdelayed())
                self.morphemelist.append(CONJUNCTCENTRALI(self.subj))
                return
            if self.mode == 'prohibitative':
                if self.subj == p21:
                    self.morphemelist.append(Si())
                    self.morphemelist.append(Wnegative())
                else:
                    self.morphemelist.append(Ke())
            if self.mode in ['neutral', 'prohibitative']:
                if self.subj == p2:
                    self.morphemelist.append(Nimperative())
                elif self.subj == p2p:
                    self.morphemelist.append(Og())
                elif self.subj == p21:
                    self.morphemelist.append(Daa())
            return
        else:
            if not self.polarity:
                self.morphemelist.append(Si())
            if self.dubitative and self.conjunct:
                self.morphemelist.append(Wdubitative())
            if self.conjunct:
                if self.subj == p3p:
                    if (self.polarity) or (not self.polarity and self.dubitative):
                        if not self.subj == self.focus:
                            self.morphemelist.append(Waa())
                elif self.subj.obviacy:
                    self.morphemelist.append(Ni_animate())
            if not self.polarity:
                self.morphemelist.append(Wnegative())
            if self.order == 'independent':
                self.morphemelist.append(INDEPENDENTCENTRALI(self.subj))
            if self.conjunct:
                self.morphemelist.append(CONJUNCTCENTRALI(self.subj))
                if not self.polarity and (not self.dubitative):
                    if self.subj == p3p:
                        if not self.subj == self.focus:
                            self.morphemelist.append(Waaw())
            if self.preterite:
                self.morphemelist.append(Ban())
            if self.dubitative and not self.pretdub:
                self.morphemelist.append(Dog())
            if self.order == 'independent':
                if self.subj.obviacy:
                    self.morphemelist.append(An_())
                if self.subj == p3p:
                    self.morphemelist.append(Ag_())
    def vii_select(self):
        if self.type is None:
            self.type = 'vii'
        if not self.polarity:
            self.morphemelist.append(Sin())
        if self.subj.obviacy:
            self.morphemelist.append(Ni_inanimate())
        elif not self.polarity and not(self.dubitative and self.order == 'independent'):
            self.morphemelist.append(Wnegative())
        if self.dubitative and self.conjunct:
            self.morphemelist.append(Wdubitative())
        if self.conjunct:
            self.morphemelist.append(G())
        else:
            self.morphemelist.append(W3rdperson())
        if self.preterite:
            self.morphemelist.append(Ban())
        if self.dubitative and not self.pretdub:
            self.morphemelist.append(Dog())

        if self.subj.plurality and self.order == 'independent':
            if (not self.polarity) and (not self.subj.obviacy) and self.mode == 'neutral':
                return
            else:
                self.morphemelist.append(An_())
    def vta_select(self):
        if self.type is None:
            self.type = 'vta'
        if self.subj == p1p and self.obj in [p2, p2p]:
            self.subj= pX
        elif not self.subj.animacy:
            self.morphemelist.append(Go())
            self.subj, self.obj = self.obj, self.subj
            self.vti_select()
            return
        if PRIMACY(self.subj) > PRIMACY(self.obj):
            self.primary = self.subj
            self.secondary = self.obj
            self.direct, self.inverse = (True, False)
        else:
            self.primary = self.obj
            self.secondary= self.subj
            self.direct, self.inverse = (False, True)
        if self.obj == p1p and self.subj.person == 2:
            #Accounts for 2, 2p > 1p being inverse form despinte 1p getting priority
            #in person marking
            self.inverse, self.direct = (False, True)
        #Personal Prefix Selection
        if self.order == 'independent' and self.subj not in [pX, p0, p0p, p0o, p0op]:
            if self.subj.person == 2 or self.obj.person == 2:
                self.morphemelist.insert(0, Gi())
            elif self.primary.person == 1:
                self.morphemelist.insert(0, Ni())
            elif self.primary.person == 3:
                self.morphemelist.insert(0, O())
        #Theme sign selection
        if self.subj.locality and self.obj.obviacy:
            #accounts for the imaa forms
            self.morphemelist.append(M())
        #All of the logic for conjugating conjunct and independent verbs
        if self.conjunct or self.independent:
            #Theme signs are chosen here
            if self.direct:
                if self.obj.locality:
                    if self.subj.person == 1:
                        self.morphemelist.append(N1stperson())
                    elif self.subj.person == 2:
                        self.morphemelist.append(I())
                elif not self.obj.locality:
                    self.morphemelist.append(Aa())
            #Inverse forms
            elif self.inverse:
                if self.subj == pX:
                    self.morphemelist.append(Goo())
                elif self.subj.locality:
                    if self.obj.locality:
                        if self.subj.person == 1:
                            self.morphemelist.append(N1stperson())
                        elif self.subj.person == 2:
                            self.morphemelist.append(I())
                elif self.conjunct and self.obj.locality:
                    if self.obj.person == 2:
                        #Accounts for forms like -ik, -inang, and -ineg
                        self.morphemelist.append(N1stperson())
                    elif self.obj.person == 1:
                        #accounts for forms like -id and -iyangid
                        self.morphemelist.append(I())
                else:
                    self.morphemelist.append(Go())
            #Branches to the VAI conjugator if the subject is indefinite
            #Except for the conjunct X>3, 3' forms with theme sign Ind
            if self.subj == pX and not (self.conjunct and not self.obj.locality):
                self.subj = self.obj
                self.vai_select()
                return
            if not self.polarity:
                self.morphemelist.append(Si())
            if self.conjunct and self.dubitative:
                self.morphemelist.append(Wdubitative())
                self.wdindex = len(self.morphemelist) - 1
            #Waa Selection
            if self.conjunct:
                if self.primary == p3p and ((self.polarity) or ((not self.polarity) and (self.dubitative))):
                    #accounts for the siwaag form that occurs in negative dubitative conjunct instead of sigwaa
                    self.morphemelist.append(Waa())
            if not self.polarity:
                self.morphemelist.append(Wnegative())
                self.windex = len(self.morphemelist) - 1
            if self.order == 'independent':
                if self.primary.locality and (not self.secondary.locality) and self.primary.plurality:
                    self.morphemelist.append(INDEPENDENTCENTRALIII(self.primary))
                if self.primary == p3p:
                    self.morphemelist.append(Waaw())
                if self.primary.locality and self.secondary.locality:
                    self.morphemelist.append(INDEPENDENTCENTRALI_(self.primary))
            if self.conjunct:
                if self.primary.locality and not self.secondary.locality or self.subj == pX:
                    if self.obj in [p1, p2]:
                        if self.obj == p2 and not self.dubitative:
                            self.morphemelist.append(K2ndperson())
                        else:
                            self.morphemelist.append(D())
                    else:
                        self.morphemelist.append(CONJUNCTCENTRALII(self.primary))
                if self.primary.locality and self.secondary.locality:
                    if self.subj.person == 2:
                        self.morphemelist.append(CONJUNCTCENTRALIII(self.primary))
                    else:
                        self.morphemelist.append(CONJUNCTCENTRALIV(self.primary))
                if not self.primary.locality and not self.secondary.locality:
                    self.morphemelist.append(D())
            if ((self.secondary == p3p and not (self.secondary == self.focus)  or
                    ((self.primary == p3p and not self.primary == self.focus) and (not self.polarity) and (not self.dubitative))) and self.conjunct):
                    self.morphemelist.append(Waaw())
            if self.preterite:
                    self.morphemelist.append(Ban())
            if self.dubitative and not self.pretdub:
                    self.morphemelist.append(Dog())
            if self.order == 'independent':
                    if self.secondary == p3op:
                        self.morphemelist.append(Ah_())
                    elif self.secondary == p3o:
                        self.morphemelist.append(An_())
                    elif self.secondary == p3p:
                        self.morphemelist.append(Ag_())
        self.classlist = [type(morpheme) for morpheme in self.morphemelist]
        if not self.polarity:
            if Aa in self.classlist:
                if any([m in self.classlist for m in [Naan, Daa, Waaw]]) and self.order == 'independent':
                    self.morphemelist.insert(self.windex + 1 , Aa())
                if self.dubitative and self.conjunct:
                    if any([m in self.classlist for m in [Waa]]):
                        self.morphemelist.insert(self.wdindex + 1 , Aa())
                    elif any([m in self.classlist for m in [Ag, Ad, Angid, Aang, Ang, Egw, Ind]]):
                        self.morphemelist.insert(self.wdindex+1, Aa())
            elif N1stperson in self.classlist:
                self.morphemelist.insert(self.windex, N1stperson())
                if self.order == 'independent':
                    self.morphemelist.insert(self.windex+2, N1stperson())
        elif self.imperative:
            #Here is the theme sign logic for imperative verbs
            if self.obj.person == 1:
                #First person object verb forms have the theme signs I and Shi
                self.morphemelist.append(I())
                self.morphemelist.append(Shi())
                if self.obj == p1p and self.mode == 'neutral':
                    self.morphemelist.append(Aam())
            else:
                #All VTA imperative forms with 2 exceptions that act on nonlocal persons
                #Have the direct theme sign Aa
                if self.mode == 'neutral':
                    #According to your data palatalizing i is only found
                    #in the second person singular neutral imperative forms
                    #and not second person plural,
                    #miizh vs miinik
                    if self.subj == p2:
                        self.morphemelist.append(I())
                        return
                    elif self.subj == p2p:
                        self.morphemelist.append(Og())
                        return
                    elif self.subj == p21:
                        self.morphemelist.append(Aa())
                else:
                    self.morphemelist.append(Aa())
            if self.mode == 'delayed':
                self.morphemelist.append(Wdelayed())
                self.morphemelist.append(Kdelayed())
                #Delayed verb forms use the conjunct theme signs an, ang, and egw to mark
                #The major person, and have no morphemes following these
                if self.obj == p1p:
                    self.morphemelist.append(Ang())
                else:
                    self.morphemelist.append(CONJUNCTCENTRALI(self.primary))
                return
            elif self.mode == 'prohibitative':
                ke = False
                if self.primary == p21:
                    self.morphemelist.append(Si())
                    self.morphemelist.append(Wnegative())
                else:
                    self.morphemelist.append(Ke())
                    ke = True
                if self.primary == p2p:
                    self.morphemelist.append(Og())
                elif self.primary == p1p:
                    self.morphemelist.append(Aang())
                if ke:
                    self.morphemelist.append(En())
            if self.subj == p21 and self.mode in ['neutral', 'prohibitative']:
                self.morphemelist.append(Daa())
                self.morphemelist.append(PERIPHERALS[self.secondary])



    def vti_select(self):
        if self.type is None:
            self.type = 'vti'
        if self.type == VTI2:
            self.morphemelist.append(Am())
            self.lemma.form.pop()
            self.lemma.form.pop()
        if self.conjunct:
            self.vai_select()
        if self.order == 'independent':
            if self.subj.person == 1:
                self.morphemelist.insert(0, Ni())
            elif self.subj.person in [21, 2]:
                self.morphemelist.insert(0, Gi())
            elif self.subj.person == 3:
                self.morphemelist.insert(0, O())
            if not self.polarity:
                self.morphemelist.append(Si())
                self.morphemelist.append(Wnegative())
            self.morphemelist.append(INDEPENDENTCENTRALII(self.subj))
            if self.subj.obviacy:
                self.morphemelist.append(Ni_animate())
            if self.preterite:
                self.morphemelist.append(Ban())
            if self.dubitative and not self.pretdub:
                self.morphemelist.append(Dog())
            if self.obj in [p0p, p0op, p3o]:
                self.morphemelist.append(An_())
            if self.obj == p3p:
                self.morphemelist.append(Ag_())
            if self.obj == p3op:
                self.morphemelist.append(Ah_())

    def assemble(self):
        if self.focus == p3p:
            self.morphemelist.append(Ag_())
        elif self.focus in [p3o, p0p, p0op]:
            self.morphemelist.append(An_())
        elif self.focus == p3op:
            self.morphemelist.append(Ah_())
        if type(self.morphemelist[-1]) == Wnegative:
            self.morphemelist.append(Nnegativeaugment())
        elif type(self.morphemelist[-1]) in [W3rdperson, Local_singular] and \
             type(self.morphemelist[-2]) == Wnegative:
                self.morphemelist.pop()
                self.morphemelist.append(Nnegativeaugment())
        for morpheme in self.morphemelist:
            morpheme.prep(self)
            morpheme.mutate()
        for morpheme in self.morphemelist:
            self.form.extend(morpheme.form)
        apocope(self)
        final_w_loss(self)
        if (not any([type(morpheme) == D or type(morpheme) == G for morpheme in self.morphemelist])) and self.pretdub:
            self.form = list('-')
