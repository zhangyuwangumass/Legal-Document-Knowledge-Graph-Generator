#coding=utf-8
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

inst_map = json.load(open('inst_map.txt', 'r'))
o = open('corporus.txt', 'w')

for i in inst_map.values():
    for l in i['name']:
        o.write(l + ' ')
    o.write('\n')
