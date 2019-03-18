#coding=utf-8
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

nodes = []
nodemap = {}
edges = []

f = open('0.txt', 'r')

ind = 0
for l in f:
    lj = json.loads(l)
    nodes.append({"name": lj[1]})
    nodemap[lj[0]] = ind
    ind += 1

type = ['案件', '地区', '时间', '机构', '当事人', '辩护人', '代理律师']

#关系      代号    参数
#相等关系   0      0~1，概率
#当事关系   1      0 原告 1 被告 2 公诉机关 3 法院 4 律师 5 代理人 6 法务人员
#诉讼关系   2      0 被诉 1 起诉
#辩护关系   3      0 被辩护 1 辩护
#代表关系   4      0 被代表 1 代表 2 被委托（代理） 3 委托（代理）
rela = {"2_1": "起诉", "3_1": "辩护", "4_1": "代表", "4_3": "委托"}

for k in range(3, 7):
    f = open(str(k) + '.txt', 'r')

    for l in f:
        lj = json.loads(l)
        if lj[2].has_key('name'):
            nodes.append({"name": type[k] + '   ' + lj[2]['name'], "type": k})
            nodemap[lj[1]] = ind
        ind += 1

for k in range(3, 7):
    f = open(str(k) + '.txt', 'r')
    for l in f:
        lj = json.loads(l)
        edges.append({"source": nodemap[lj[0][0]], "target": nodemap[lj[1]], "rela": ""})
        for i in lj[3].items():
            if rela.has_key(i[1]):
                relation = rela[i[1]]
            else:
                relation = ''
            edges.append({"source": nodemap[lj[1]], "target": nodemap[i[0]], "rela": relation})

o1 = open('nodes_reduced.json', 'w')
o1.write(json.dumps(nodes, ensure_ascii=False).replace('\"name\"', 'name').replace('\"type\"', 'type'))

o2 = open('edges_reduced.json', 'w')
o2.write(json.dumps(edges, ensure_ascii=False).replace('\"source\"', 'source').replace('\"target\"', 'target').replace('\"rela\"', 'rela'))