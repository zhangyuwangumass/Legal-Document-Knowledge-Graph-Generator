#coding=utf-8
import sys
import re
f = open(sys.argv[1] + '_out', 'r')
t = open(sys.argv[1] + '_title', 'w')
b = open(sys.argv[1] + '_body', 'w')

line_count = 0
pivot = 0
list = []
is_serial = False

for l in f:
    line_count += 1
    list.append(l)

    if l == '\n':
        for line in list[:pivot]:
            t.write(line)
        t.write('\n\n')
        for line in list[pivot:-1]:
            b.write(line)
        b.write('正文结束\n\n\n')
        list = []
        is_serial = False
        line_count = 0
        pivot = 0
    elif is_serial:
        if re.match('公诉机关', l) or re.match('原公诉机关', l):
            pivot = line_count
        else:
            pivot = line_count - 1
        is_serial = False
    elif re.match('^（', l):
        is_serial = True
