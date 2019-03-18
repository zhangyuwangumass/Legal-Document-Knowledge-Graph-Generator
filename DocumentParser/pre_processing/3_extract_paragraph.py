#coding=utf-8
from __future__ import division
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import re
import json

'''对原始文件进行预处理并分类
    raw 设定原始文件存放路径，pre_out 设置预处理文件存放路径，class_out 存放分类后文件路径，clear_pre_out 和clear_class_out 决定是否对指定路径内已有文件进行进行清理
    '''


def filter(raw, out, ex):
    raw = raw
    out = out
    pros_keywords = ['原告', '上诉人', '起诉人', '申请人', '申请执行人']
    def_keywords = ['被告', '被上诉人', '被起诉人', '被申请人', '被执行人', '罪犯']
    neu_keywords = ['委托', '法定代表', '辩护', '代表', '负责人', '原审', '第三人']
    lawmen_keywords = ['审判长', '审判员', '代理审判员', '人民陪审员']
    end_keyword = '书记员'

    f = open(raw, 'r')
    o = open(out, 'w')
    ex = open(ex, 'a')
    pf = False
    rf = False
    ef = False

    content_list = []
    for l in f:
        if l == '\n':
            for line in content_list:
                print line
            try:
                for item in content_list:
                    if ef:
                        if re.match(end_keyword.decode('string_escape'), item):
                            o.write(item)
                            '''print item'''
                            break
                        for keyword in lawmen_keywords:
                            if re.match(keyword.decode('string_escape'), item):
                                '''print item'''
                                o.write(item)
                                break
                    else:
                        is_flag = False
                        if not rf:
                            for keyword in pros_keywords:
                                if re.match(keyword.decode('string_escape'), item):
                                    is_flag = True
                                    pf = True
                                    '''print item'''
                                    o.write(item)
                                    break

                        if not is_flag:
                            for keyword in def_keywords:
                                if re.match(keyword.decode('string_escape'), item):
                                    rf = True
                                    is_flag = True
                                    '''print item'''
                                    o.write(item)
                                    break

                        if not is_flag:
                            for keyword in neu_keywords:
                                if re.match(keyword.decode('string_escape'), item):
                                    is_flag = True
                                    '''print item'''
                                    o.write(item)
                                    break

                        if not is_flag and (pf or rf):
                            ef = True
                        if not pf and not rf:
                            '''print item'''
                            o.write(item)
                o.write('\n')
            except (Exception):
                '''print 'exception occured'''''
                ex.write(l)
                o.write('\n')
                '''将有问题的文件写入exception.txt'''
                pass

            pf = False
            rf = False
            ef = False
            content_list = []
        else:
            content_list.append(l)


filter(sys.argv[1] + '_clean', sys.argv[1] + '_out', 'exception')
