#coding=utf-8

keywords = ['case', 'loco', 'time', 'person', 'inst', 'gender', 'ethic', 'social', 'lawyer', 'lawfirm', 'lawyernum', 'lawworker', 'court', 'serial']
sf = open('data/single_search_map.txt', 'w')#不重名节点表
df = open('data/duplicate_search_map.txt', 'w')#重名节点表
sv = 0#总结点数
dv = 0#重名节点数
sdict = {}#不重名字典
ddict = {}#重名字典

for i in range(13):
    inf = open('data/' + keywords[i] + '_map.txt', 'r')
    for l in inf:
        sv += 1
        ls = l.split('&')
        if len(ls) < 2:
            continue
        name = ls[1].rstrip()
        if sdict.has_key(name):
            ddict[name] = sdict[name] + ' ' + ls[0]
            sdict.pop(name)
            dv += 2
        elif ddict.has_key(name):
            ddict[name] += (' ' + ls[0])
            dv += 1
        else:
            sdict[name] = ls[0]

sf.write('Single vertices number: ' + str(sv - dv) + '\n')
for j in sdict.items():
    sf.write(j[0] + '&' + j[1] + '\n')

df.write('Duplicate vertices number: ' + str(dv) + '\n')
for j in ddict.items():
    df.write(j[0] + '&' + j[1] + '\n')