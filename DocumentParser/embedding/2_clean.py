#coding=utf-8
import sys

f = open(sys.argv[1] + '_lac', 'r')
o = open(sys.argv[1] + '_split', 'w')

for l in f:
    if l != '\n':
        '''是否需要保留标点符号信息？'''
        '''o.write(l.replace(' ', '\n').replace('（', '').replace('）', '').replace('，', '').replace('：', '').replace('；', '').replace('。', '').replace('、', ''))'''
        o.write(l.replace(' ', '\n'))