#import libraries
import re
import os
from collections import defaultdict

# Constants
FILE_NAME = 'BIRD_v210_1.txt'
WIDTH = 5616
HEIGHT = 3744
S_DIR = 'xml/'
IMG_FOLDER = 'imgs'

# XML templates for annotation
obj_xml = '''\
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

# Default value function for defaultdict
def def_value():
    return []

# Read the annotation file
with open(FILE_NAME) as f:
    ano_list = f.readlines()

# Define regex patterns
pattern_img = 'IMG.*.jpg'
pattern_ano = '\d*[\d,]+[bun]'
f_img = re.compile(pattern_img)
f_ano = re.compile(pattern_ano)

# Initialize variables
filename = ''
ano = defaultdict(def_value)

# Function to add annotations to dictionary
def ano_dic(s):
    ano[filename].append(s.replace('\n', ''))

# Parse the annotation list
for s in ano_list:
    if f_img.match(s):
        filename = s.replace('\n', '')
    elif f_ano.match(s):
        ano_dic(s)

# Create directory for XML files if it doesn't exist
new_path = S_DIR
if not os.path.exists(new_path):
    os.mkdir(new_path)

# Function to convert annotation string to XML format
def ano2xml(s):
    l = s.split(',')
    if l[4] == 'b':
        obj = 'birds'
    elif l[4] == 'n':
        obj = 'non-birds'
    else:
        obj = 'undefined-object'
    return obj_xml.format(name=obj, xmin=l[0], ymin=l[1], xmax=int(l[0])+int(l[2]), ymax=int(l[1])+int(l[3]))

# Function to write XML file
def write2xml(l, s):
    with open(S_DIR + s[:-4] + '.xml', mode='w') as f:
        f.write(top.format(folder=IMG_FOLDER, f_name=s, width=WIDTH, height=HEIGHT) + '\n'.join(l) + bottom)

# Generate and write XML files
for s in ano:
    xml = []
    for t in ano[s]:
        xml.append(ano2xml(t))
    write2xml(xml, s)
