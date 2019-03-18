#coding=utf-8
import re
import sys

t = open('content_title_2.txt', 'r')
b = open('content_lac_2.txt', 'r')
m = open('content_merge_2.txt', 'w')

l = t.readline()
line = b.readline()

title = []
body = []

while(l):
    if l == '标题结束\n':
        while(line and line != '\n'):
            body.append(line)
            line = b.readline()
        while(line and line == '\n'):
            line = b.readline()
        if len(title) > 0:
            for i in title:
                m.write(i)
            for j in body:
                m.write(j)
            m.write('\n\n')
        title = []
        body = []
    elif l != '\n':
        title.append(l)
    l = t.readline()