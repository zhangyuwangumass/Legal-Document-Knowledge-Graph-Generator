#coding=utf-8
import sys

f = open(sys.argv[1], 'r')
o = open(sys.argv[1] + '_clean', 'w')

for l in f:
    o.write(l.replace('　', '').replace(' ', '').replace('：', '').replace(',', '，'))
