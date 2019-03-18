#coding=utf-8
import re
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
import json

f = open(sys.argv[1], 'r')
o = open('content', 'w')

for l in f:
    js = json.loads(l)
    print (js['document'])['content']
    o.write((js['document'])['content'].replace('\b', '\n') + '\n\n')
