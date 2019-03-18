#coding=utf-8
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def load_graph():
    # 相等关系   0      0~1，概率
    # 当事关系   1      0 原告 1 被告 2 律师 3 代表人 4 代理人 5 审判长 6 审判员 7 法院
    # 诉讼关系   2      0 被诉 1 起诉
    # 辩护关系   3      0 被辩护 1 辩护
    # 代表关系   4      0 被代表 1 代表 2 被委托（代理） 3 委托（被代理）
    # 法院关系   5      0 审判长 1 审判员
    # 地点关系   6      0 住所地 1 出生地 2 户籍地
    # 时间关系   7      0 出生日期 1 判决日期
    # 属性关系   8      0 性别 1 民族 2 机构社会编号 3 律所 4 律师执业证号

    # 第一步：加载案件编号map
    case_graph = json.load(open('case_graph.txt', 'r'))
    # 第二步：加载法院编号map
    court_graph = json.load(open('court_graph.txt', 'r'))

    nodes_graph = {}

    p_f = open('person_graph.txt', 'r')

    for l in p_f:
        lj = json.loads(l)
        id = lj[1]
        nodes_graph[id] = lj

    i_f = open('institute_graph.txt', 'r')

    for l in i_f:
        lj = json.loads(l)
        id = lj[1]
        nodes_graph[id] = lj

    loco_graph = json.load(open('loco_graph.txt', 'r'))
    time_graph = json.load(open('time_graph.txt', 'r'))
    gender_graph = json.load(open('gender_graph.txt', 'r'))
    ethic_graph = json.load(open('ethic_graph.txt', 'r'))
    social_graph = json.load(open('social_graph.txt', 'r'))
    lawfirm_graph = json.load(open('lawfirm_graph.txt', 'r'))
    lawyernum_graph = json.load(open('lawyernum_graph.txt', 'r'))

    nodes_graph = dict(nodes_graph, **case_graph)
    nodes_graph = dict(nodes_graph, **court_graph)
    nodes_graph = dict(nodes_graph, **loco_graph)
    nodes_graph = dict(nodes_graph, **time_graph)
    nodes_graph = dict(nodes_graph, **gender_graph)
    nodes_graph = dict(nodes_graph, **ethic_graph)
    nodes_graph = dict(nodes_graph, **social_graph)
    nodes_graph = dict(nodes_graph, **lawfirm_graph)
    nodes_graph = dict(nodes_graph, **lawyernum_graph)
    return nodes_graph
