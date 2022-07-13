#import libraries
import re
import os
from collections import defaultdict


FILE_NAME = 'BIRD_v210_1.txt'
WIDTH  = 5616
HEIGHT = 3744
S_DIR = 'xml/'
IMG_FOLDER = 'imgs'


#XML formats
obj_xml ='''\
    <object>
        <name>{name}</name>
        <difficult>0</difficult>
        <bndbox>
            <xmin>{xmin}</xmin>
            <ymin>{ymin}</ymin>
            <xmax>{xmax}</xmax>
            <ymax>{ymax}</ymax>
        </bndbox>
    </object>'''

top = '''\
<annotation>
    <folder>{folder}</folder>
    <filename>{f_name}</filename>
    <size>
        <width>{width}</width>
        <height>{height}</height>
        <depth>3</depth>
    </size>\n'''

bottom = '''\
\n</annotation>'''


def def_value():
    return []

with open(FILE_NAME)as f:
    ano_list=f.readlines()

pattern_img = 'IMG.*.jpg'
pattern_ano = '\d*[\d,]+[bun]'
f_img = re.compile(pattern_img)
f_ano = re.compile(pattern_ano)

filename = ''
ano = defaultdict(def_value)
def ano_dic(s):
    ano[filename].append(s.replace('\n', ''))

for s in ano_list:
    if f_img.match(s):
        filename = s.replace('\n', '')
    elif f_ano.match(s):
        ano_dic(s)


new_path = 'xml'
if not os.path.exists(new_path):
    os.mkdir(new_path)


def ano2xml(s):
    l = s.split(',')
    if l[4] == 'b':
        obj = 'birds'
    elif l[4] == 'n':
        obj = 'non-birds'
    else:
        obj = 'undefined-object'
    return obj_xml.format(name=obj, xmin=l[0], ymin=l[1], xmax=l[0]+l[2], ymax=l[1]+l[3])

def write2xml(l, s):
    with open(S_DIR+s[:-4]+'.xml',mode='w') as f:
        f.write(top.format(folder=IMG_FOLDER, f_name=s, width=WIDTH, height=HEIGHT)+'\n'.join(l)+bottom)

for s in ano:
    xml = []
    for t in ano[s]:
        #print(ano2xml(t))
        xml.append(ano2xml(t))
    write2xml(xml, s)