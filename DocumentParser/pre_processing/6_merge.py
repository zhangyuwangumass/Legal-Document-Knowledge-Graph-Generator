#coding=utf-8
import re
import sys

t = open(sys.argv[1] + '_title', 'r')
b = open(sys.argv[1] + '_lac', 'r')
m = open(sys.argv[1] + '_merge', 'w')

switch = False
l = t.readline()
line = b.readline()

while(l):
    t.flush()
    if l != '\n':
        if not switch:
            m.write(l)
        else:
            while(line and line != '\n'):
                m.write(line)
                line = b.readline()
            while(line and line == '\n'):
                line = b.readline()
            m.write('\n')
            switch = False
            m.write(l)
            b.flush()
    else:
        switch = True
    l = t.readline()

while(line and line != '\n'):
    m.write(line)
    line = b.readline()
m.write('\n')
