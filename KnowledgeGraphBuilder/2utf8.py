#coding=utf-8

f = open('nodes.json', 'r')
o = open('nodes_utf8.json', 'w')

for l in f:
    o.write(l.encode('utf-8'))