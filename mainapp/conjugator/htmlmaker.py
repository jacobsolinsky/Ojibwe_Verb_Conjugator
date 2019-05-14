import numpy as np
import itertools as it
import os
from OjibweMorphology import *
#types


def makepage(body):
    pagetext =  """

<!DOCTYPE html>
<html>
<head>
  <style>
html{
    font-family:sans-serif;
    -ms-text-size-adjust:100%;
    -webkit-text-size-adjust:100%
}
table{
    border-collapse:collapse;
    border-spacing:0
}
td,th{
    padding:0
    border-botoom: 1px solid grey;
empty-cells: hide;
text-align: center;
font-family: "Arial", sans-serif;
font-size: 200%;
}
th {
background-color: #ECE5DB;
}
td {
background-color: white;
}
body {
      background-image: url('https://ojibwe.lib.umn.edu/assets/background-9be1f6579e0a17b66890ade0d35a84e78e104835b2bc605503e25d9ba0c8bd99.jpg') ;
      background-repeat:repeat-x;
      background-color: #ECE5DB;
      width:80%;
      margin-left:auto;
      margin-right:auto;
      margin-top:400px
}
caption {
        font-family: "Arial", sans-serif;
        text-align: left;
        font-size: 100%;
}

.flex-container {
  display: flex;
 flex-direction: column
}
.flex-container > .flex-container {
  display: flex;
flex-direction: row
}

.flex-container > div {
  margin: 10px;
  padding: 20px;
font-size: 30px;

}
</style>
</head>
<body>""" + body + """
</body>
</html>
"""

    with open('/Users/jacobsolinsky/programming/python/htmlpractice.html', 'w+') as pik:
        pik.write(pagetext)
    os.system("open -a 'Google chrome' '/Users/jacobsolinsky/programming/python/htmlpractice.html'")
    return pagetext



class Attributes:
    def __init__(self, attributes):
        self.attributes = attributes
    def __str__(self):
        result = ''
        for key, value in self.attributes.items:
            result += f' {key}={value}'

class Tag:
    def __init__(self, tag, content = '', attributes = ''):
        self.tag = tag
        self.content = content
        self.contentlist = []
        self.attributes = attributes
    def __str__(self):
        return f'<{self.tag} {self.attributes}>{self.content}</{self.tag}>'
    def append(self, tag):
        self.contentlist += str(tag)

class Th(Tag):
    def __init__(self, content = '', attributes = ''):
        super().__init__( tag = 'th', content=content, attributes=attributes)
class Td(Tag):
    def __init__(self, row, funcname, kwarglist, attributes = ''):
        self.funcname = funcname
        self.row = row
        self.kwarglist = kwarglist + self.row.kwarglist
        self.kwarglist = ','.join(self.kwarglist)
        content = f"""{funcname}({self.kwarglist})()"""
        content = eval(content)
        super().__init__(content=content, attributes=attributes, tag = 'td')
class Contentrow(Tag):
    def __init__(self, table, funcname, ci, attributes = ''):
        self.funcname = funcname
        self.table = table
        self.ci = ci
        self.kwarglist =[]
        self.kwarglist += self.table.kwarglist
        self.contentlist = []
        #Append headers and row-level arguments
        for i in range(len(self.table.dim2list)):
            width = self.table.dim2widthlist[i]
            length = self.table.dim2lenlist[i]
            number = (ci % (width*length)) // (width)
            self.kwarglist.append(f'{self.table.dim2list[i].keyword}="{self.table.dim2list[i].argdict[number][0]}"' )
            if ci % width == 0:
                content = self.table.dim2list[i].argdict[number][1]
                self.contentlist = [str(Th( content = content, attributes = f'rowspan="{width}"'))] + self.contentlist
        #Append Entry-level kwargs
        for ri in range(np.cumprod(self.table.dim1lenlist)[-1]):
            tagkwarglist = []
            for i in range(len(self.table.dim1list)):
                width = self.table.dim1widthlist[i]
                length = self.table.dim1lenlist[i]
                number = (ri % (width*length)) // (width)
                tagkwarglist.append(f'{self.table.dim1list[i].keyword}="{self.table.dim1list[i].argdict[number][0]}"')
            self.append(Td(self, funcname = self.funcname, kwarglist = tagkwarglist))
        self.content = ''.join(self.contentlist)
        super().__init__(tag = 'tr', content = self.content)


class Headrow(Tag):
    def __init__(self, table, hi, attributes = ''):
        self.contentlist = []
        self.table = table
        if hi == len(self.table.dim1list):
            self.append(Th(content = self.table.dim2list[0].dimname +' ▼'))
            self.content = ''.join(self.contentlist)
            super().__init__(tag = 'tr', content = self.content)
            return
        dim = list(reversed(self.table.dim1list))[hi]
        dimwidth = list(reversed(self.table.dim1widthlist))[hi]
        dimrepeat = list(reversed(self.table.dim1repeatlist))[hi]
        dimlen = list(reversed(self.table.dim1lenlist))[hi]
        if hi == len(self.table.dim1list) - 1:
            for dim2 in list(reversed(self.table.dim2list))[:-1]:
                self.append(Th(content = dim2.dimname, attributes = 'rowspan="2"'))
            self.append(Th(content = dim.dimname + ' ▶'))
        elif hi == 0:
            self.append(Th(attributes = f'rowspan="{len(self.table.dim1list)-1}" colspan="{len(self.table.dim2list)-1}"'))
        if not hi == len(self.table.dim1list) - 1:
            self.append(Th(content = dim.dimname))
        for i in range(dimlen * dimrepeat):
            number = (i % (dimlen))
            arg = dim.argdict[number][1]
            if hi == len(self.table.dim1list) - 1:
                thiswidth = 2
            else:
                thiswidth = 1
            self.append(Th(content = arg, attributes = f"colspan='{dimwidth}' rowspan = '{thiswidth}'"))
        self.content = ''.join(self.contentlist)
        super().__init__(tag = 'tr', content = self.content)
class Table(Tag):
    def __init__(self,  dim1list, dim2list, attributes = '', kwarglist = [], caption = None,  page = None, funcname = "Verb"):
        if page is not None:
            self.kwarglist = page.kwarglist +  kwarglist
        else:
            self.kwarglist = kwarglist
        self.page = page
        self.caption = Tag('caption', content = caption)
        self.contentlist = []
        self.append(self.caption)
        self.funcname = funcname
        self.dim1list = dim1list
        self.dim1lenlist = [len(dim1) for dim1 in dim1list]
        self.dim1widthlist = []
        for i, nn in enumerate(dim1list):
            width = np.cumprod(self.dim1lenlist[:i])
            self.dim1widthlist.append(width[-1] if width else 1)
        self.dim1repeatlist = []
        for i, nn in enumerate(dim1list):
            repeat = np.cumprod(self.dim1lenlist[i+1:])
            self.dim1repeatlist.append(repeat[-1] if repeat else 1)
        self.dim2lenlist = [len(dim2) for dim2 in dim2list]
        self.dim2list = dim2list
        self.dim2widthlist = []
        for i, nn in enumerate(dim2list):
            width = np.cumprod(self.dim2lenlist[:i])
            self.dim2widthlist.append(width[-1] if width else 1)
        self.dim2repeatlist = []
        for i, nn in enumerate(dim2list):
            repeat = np.cumprod(self.dim2lenlist[i+1:])
            self.dim2repeatlist.append(repeat[-1] if repeat else 1)
        hino = len(self.dim1list)
        cino = np.cumprod(self.dim2lenlist)[-1]
        for hi in range(hino+1):
            self.append(Headrow(self, hi))
        for ci in range(cino):
            self.append(Contentrow(self, funcname = self.funcname, ci = ci))
        self.content = ''.join(self.contentlist)
        super().__init__(tag = 'table', content = self.content)
        def __str__(self):
            return f'<{self.tag} {self.attributes}>{self.content}</{self.tag}>'

class Page(Tag):
    def __init__(self,  layout, dim3list, kwarglist, funcname = 'Verb'):
        self.funcname = funcname
        self.dim3list = dim3list
        self._kwarglist = kwarglist
        self.dim3keywordlist = [dim3.keyword for dim3 in self.dim3list]
        self.dim3arglist = [dim3.argdict for dim3 in self.dim3list]
        self.layout = layout
        self.contentlist = []
        self.funcname = funcname
        for pairs in it.product(*self.dim3arglist):
            self.kwarglist = [f'{keyword}="{arg[0]}"' for keyword, arg in zip(self.dim3keywordlist, pairs)]
            self.kwarglist += self._kwarglist
            self.title = ', '.join([f'{arg[1]} {keyword}' for keyword, arg in zip(self.dim3keywordlist, pairs)])
            group = eval('f"""' + self.layout + '"""')
            self.append(f'<div class = "group">{group}</div>')
    def __str__(self):
        return ''.join(self.contentlist)

class Littlepage(Tag):
    def __init__(self,  kwarglist):
        self.kwarglist = kwarglist




class Dimension:
    def __init__(self, keyword, dimname, argdict):
        self.keyword = keyword
        self.dimname = dimname
        self.argdict = argdict
    def __len__(self):
        return len(self.argdict)
animatesubject = Dimension('subj', 'Subject', [
        ['1','1'],
        ['2','2'],
        ['3','3'],
        ["3'","3'"],
        ['1p','1p'],
        ['21','21'],
        ['2p','2p'],
        ['3p','3p'],
        ['X','X']])
animateobject = Dimension('obj', 'Object', [
        ['1','1'],
        ['2','2'],
        ['3','3'],
        ["3'","3'"],
        ['1p','1p'],
        ['21','21'],
        ['2p','2p'],
        ['3p','3p']])
inanimatesubject = Dimension('subj', 'Subject', [
        ['0','0'],
        ["0'","0'"],
        ['0p','0p'],
        ["0'p","0'p"]])
conjinanimatesubject = Dimension('subj', 'Subject', [
        ['0','0 or 0p'],
        ["0'","0' or 0'p"]])
inanimateobject = Dimension('obj', 'Object', [
        ['0','0'],
        ["0p","0p"]])
singleinanimateobject = Dimension('obj', 'Object', [['0','0']])

reducedinanimatesubject = Dimension('subj', 'Subject', [
        ['0','0'],
        ["0p","0p"]])
vtainanimatesubbject = Dimension('subj', 'Subject', [
        ['0','0'],
        ["0p","0p"]])
indefinitesubject = Dimension('subj', 'Subject', [['X','X']])

localsubject = Dimension('subj', 'Subject', [
        ['1','1'],
        ['2','2'],
        ['1p','1p'],
        ['21','21'],
        ['2p','2p']])
localobject = Dimension('obj', 'Object', [
        ['1','1'],
        ['2','2'],
        ['1p','1p'],
        ['21','21'],
        ['2p','2p']])
nonlocalsubject = Dimension('subj', 'Subject', [
        ['3','3'],
        ['3p','3p']])
nonlocalobject = Dimension('obj', 'Object', [
        ['3','3'],
        ['3p','3p'],
         ["3'", "3'"]])
thirdobject = Dimension('obj', 'Object', [
        ['3','3'],
         ['3p','3p']])
thirdsubject = Dimension('subj', 'Subject', [
        ['3',"3 or 3'"],
         ['3p','3p']])
fourthsubject = Dimension('subj', 'Subject', [["3'","3'"]])
fourthobject = Dimension('obj', 'Object', [["3'","3'"]])
firstsubject = Dimension('subj', 'Subject', [
        ['1','1'],
        ['1p','1p']])
firstobject = Dimension('obj', 'Object', [
        ['1','1'],
        ['1p','1p']])
secondsubject = Dimension('subj', 'Subject', [
        ['2','2'],
        ['2p','2p']])
secondobject = Dimension('obj', 'Object', [
        ['2','2'],
        ['2p','2p']])
imperativesubject = Dimension('subj', 'Subject', [
        ['2','2'],
        ['2p','2p'],
        ['21','21']])
regmodes = Dimension('mode', 'Mode', [
        ['neutral', 'Neutral'],
        ['preterite', 'Preterite'],
        ['dubitative', 'Dubitative'],
        ['preterite-dubitative', 'Preterite-Dubitative']])
impmodes = Dimension('mode', 'Mode', [
        ['neutral', 'Neutral'],
        ['prohibitative', 'Prohibitative'],
        ['delayed', 'Delayed']])
orders = Dimension('order', 'Order', [
        ['independent','Independent'],
        ['conjunct', 'Conjunct'],
        ['imperative', 'Imperative']])
biorders = Dimension('order', 'Order', [
        ['independent','Independent'],
        ['conjunct', 'Conjunct']])
imporder = Dimension('order', 'Order', [['imperative', 'Imperative']])
polarities = Dimension('polarity', 'Polarity', [
        ['True','Positive'],
        ['False','Negative']])
vaiindependent = 0
vaiconjunct = 0
vaiimperative = 0


class Localdirect(Table):
    def __init__(self,  page):
            super().__init__(page = page,  dim2list = [secondsubject], dim1list = [firstobject], caption = "Local Direct")
class Localinverse(Table):
        def __init__(self,  page):
            super().__init__(page = page,  dim2list = [secondobject], dim1list = [firstsubject], caption = "Local Inverse")
class Mixeddirect(Table):
        def __init__(self,  page):
            super().__init__(page = page,  dim2list = [localsubject], dim1list=[nonlocalobject], caption = "Mixed Direct")
class Mixedinverse(Table):
        def __init__(self,  page):
            super().__init__(page = page,  dim2list = [localobject], dim1list = [nonlocalsubject], caption = "Mixed Inverse")
class Inanimateinverse(Table):
        def __init__(self,  page):
            super().__init__(page = page,  dim2list = [animateobject], dim1list = [reducedinanimatesubject], caption = "Inanimate Subject")
class Indefinitesubject(Table):
        def __init__(self,  page):
            super().__init__(page = page,  dim2list = [animateobject], dim1list = [indefinitesubject], caption = "Indefinite Subject")
class Nonlocaldirect(Table):
        def __init__(self,  page):
            super().__init__(page = page,  dim2list = [thirdsubject], dim1list = [fourthobject], caption = "Nonlocal Direct")
class Nonlocalinverse(Table):
        def __init__(self,  page):
            super().__init__(page = page,  dim2list = [thirdobject], dim1list = [fourthsubject], caption = "Nonlocal Inverse")

class Impmixed(Table):
        def __init__(self,  page):
            super().__init__(page = page,  dim1list = [imperativesubject], dim2list = [nonlocalobject, impmodes], caption = "Imperative Nonlocal")
class Implocal(Table):
        def __init__(self,  page):
            super().__init__(page = page,  dim1list = [secondsubject], dim2list = [firstobject, impmodes], caption = "Imperative Local")

class Neutvai(Table):
        def __init__(self,  page):
            super().__init__(page = page,  dim2list = [animatesubject, polarities], dim1list = [regmodes, biorders])
class Neutvtiind(Table):
        def __init__(self,  page):
            super().__init__(page = page,  dim2list = [animatesubject, polarities], dim1list = [inanimateobject, regmodes], caption = "Independent")

class Neutvticonj(Table):
        def __init__(self,  page):
            super().__init__(page = page,  dim2list = [animatesubject, polarities], dim1list = [singleinanimateobject,regmodes], caption = "Conjunct")

class Impvai(Table):
        def __init__(self,  page):
            super().__init__(page = page,  dim2list = [imperativesubject], dim1list=[impmodes], kwarglist = ['order = "imperative"'], caption = "Imperative")
class Impvti(Table):
        def __init__(self,  page):
            super().__init__(page = page,   dim2list = [imperativesubject], dim1list = [impmodes], kwarglist = ["obj=0",  'order = "imperative"'], caption = "Imperative")
class Neutvii(Table):
        def __init__(self, page):
            super().__init__(page = page,   dim2list = [inanimatesubject, polarities], dim1list = [regmodes, biorders])
vtaneutstruct =     '''
<div class="flex-container">
  <h1> {self.title} </h1>
  <div class="flex-container">
      <div>
	{Localdirect(self)}
      </div>
      <div>
	{Localinverse(self)}
      </div>
      <div>
	{Nonlocaldirect(self)}
      </div>
      <div>
	{Nonlocalinverse(self)}
      </div>
    </div>
  <div class="flex-container">
      <div>
	{Mixeddirect(self)}
      </div>
      <div>
	{Mixedinverse(self)}
      </div>
      <div>
	{Indefinitesubject(self)}
      </div>
      <div>
	{Inanimateinverse(self)}
   </div>
</div>
'''
vtaimpstruct = '''
    <div class="flex-container" >
      <div>
	{Impmixed(self)}
      </div>
       <div>
	{Implocal(self)}
      </div>
    </div>
'''


def vaioutput(lemma):
    body = str(Neutvai(Littlepage([f'lemma = "{lemma}"']))) + str(Impvai(Littlepage([f'lemma = "{lemma}"'])))
    return makepage(body)
def viioutput(lemma):
    body = str(Neutvii(Littlepage([f'lemma = "{lemma}"'])))
    return makepage(body)
def vtioutput(lemma):
    body = str(Neutvtiind(Littlepage([f'lemma = "{lemma}"', 'order = "independent"']))) +  \
    str(Neutvticonj(Littlepage([f'lemma = "{lemma}"', 'order = "conjunct"']))) + \
    str(Impvti(Littlepage([f'lemma = "{lemma}"'])))
    return makepage(body)
def vtaoutput(lemma):
    body = str(Page(kwarglist = [f'lemma = "{lemma}"'], dim3list = [biorders, regmodes, polarities], layout=vtaneutstruct)) + \
        str(Page(kwarglist = [f'lemma = "{lemma}"'], dim3list = [imporder], layout=vtaimpstruct))
    return makepage(body)
def naoutput(lemma):
    pass
def nioutput(lemma):
    pass
CALLDICT = {
    'vai':[vaioutput,{}],
    'vii':[viioutput,{}],
    'vti':[vtioutput,{}],
    'vti2':[vtioutput,{'an':True}],
    'vaio':[vtioutput,{'vaio':True}],
    'vta':[vtaoutput,{}],
    'na':[naoutput,{}],
    'nad':[naoutput,{'dependent':True}],
    'ni':[nioutput, {}],
    'nid':[nioutput, {'dependent':True}],
}
def conj_call(entry):
    """determines what function call to make to conjugate
    a given word based on its part of speech"""
    calling = CALLDICT[entry.part_of_speech]
    return calling[0](**calling[1])