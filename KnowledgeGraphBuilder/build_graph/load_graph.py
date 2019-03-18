#coding=utf-8
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#选择加载哪些子图。mode：正选或反选，mode = '+' 表示正选，mode = '-' 表示反选。如果给的keyword错误，则不会对该文件做处理
#注意：不加载所有子图时，搜索会出现找不到节点的情况，需要处理
#args: case, loco, time, person, inst, gender, ethic, social, lawyer, lawfirm, lawyernum, lawworker, court
def load_graph(graph, mode, args):
    # 相等关系   0      0~1，概率
    # 当事关系   1      0 原告 1 被告 2 律师 3 代表人 4 代理人 5 审判长 6 审判员 7 法院
    # 诉讼关系   2      0 被诉 1 起诉
    # 辩护关系   3      0 被辩护 1 辩护
    # 代表关系   4      0 被代表 1 代表 2 被委托（代理） 3 委托（被代理）
    # 法院关系   5      0 审判长 1 审判员
    # 地点关系   6      0 住所地 1 出生地 2 户籍地
    # 时间关系   7      0 出生日期 1 判决日期
    # 属性关系   8      0 性别 1 民族 2 机构社会编号 3 律所 4 律师执业证号

    files = {'case': 'case_graph.txt', 'loco': 'loco_graph.txt',
             'time': 'time_graph.txt', 'person': 'person_graph.txt',
             'inst': 'inst_graph.txt', 'gender': 'gender_graph.txt',
             'ethic': 'ethic_graph.txt', 'social': 'social_graph.txt',
             'lawyer': 'lawyer_graph.txt', 'lawfirm': 'lawfirm_graph.txt',
             'lawyernum': 'lawyernum_graph.txt', 'lawworker': 'lawworker_graph.txt',
             'court': 'court_graph.txt'}

    if mode == '+':
        for i in args:
            if files.has_key(i):
                f = open(files[i], 'r')
                fj = json.load(f)
                f.close()
                for j in fj.items():
                    graph[j[0]] = j[1]
                del fj
                print 'Successfully loaded ' + i + '_graph'
    elif mode == '-':
        for i in files.keys():
            if i not in args:
                f = open(files[i], 'r')
                fj = json.load(f)
                f.close
                for j in fj.items():
                    graph[j[0]] = j[1]
                del fj
                print 'Successfully loaded ' + i + '_graph'

#args: case, loco, time, person, inst, gender, ethic, social, lawyer, lawfirm, lawyernum, lawworker, court
def load_map(map, mode, args):
    files = {'case': 'case_map.txt', 'loco': 'loco_map.txt',
             'time': 'time_map.txt', 'person': 'person_map.txt',
             'inst': 'inst_map.txt', 'gender': 'gender_map.txt',
             'ethic': 'ethic_map.txt', 'social': 'social_map.txt',
             'lawyer': 'lawyer_map.txt', 'lawfirm': 'lawfirm_map.txt',
             'lawyernum': 'lawyernum_map.txt', 'lawworker': 'lawworker_map.txt',
             'court': 'court_map.txt'}

    if mode == '+':
        for i in args:
            if files.has_key(i):
                f = open(files[i], 'r')
                fj = json.load(f)
                f.close()
                for j in fj.items():
                    map[j[0]] = j[1]
                del fj
                print 'Successfully loaded ' + i + '_map'
    elif mode == '-':
        for i in files.keys():
            if i not in args:
                f = open(files[i], 'r')
                fj = json.load(f)
                f.close()
                for j in fj.items():
                    map[j[0]] = j[1]
                del fj
                print 'Successfully loaded ' + i + '_map'

def get_name(id, nodes_map):
    features = nodes_map[id]
    #print type(features)
    if type(features) == unicode:
        tmpname = features
    elif features.has_key('name'):
        tmpname = features['name']
    else:
        tmpname = ''
    name = ''
    if type(tmpname) == list:
        for j in tmpname:
            name += j
    else:
        name = tmpname
    return name