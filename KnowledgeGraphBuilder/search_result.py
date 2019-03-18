#coding=utf-8
import json
import sys
import load_graph
reload(sys)
sys.setdefaultencoding('utf-8')

#相等关系   0      0~1，概率
#当事关系   1      0 原告 1 被告 2 律师 3 代表人 4 代理人 5 审判长 6 审判员 7 法院
#诉讼关系   2      0 被诉 1 起诉
#辩护关系   3      0 被辩护 1 辩护
#代表关系   4      0 被代表 1 代表 2 被委托（代理） 3 委托（被代理）
#法院关系   5      0 审判长 1 审判员
#地点关系   6      0 住所地 1 出生地 2 户籍地
#时间关系   7      0 出生日期 1 判决日期
#属性关系   8      0 性别 1 民族 2 机构社会编号 3 律所 4 律师执业证号

edge_matrix = [[], ['当事人', '当事人', '律师', '代表人', '代理人', '审判长', '审判员', '法院'], ['被诉', '起诉'],
               ['被辩护', '辩护'], ['被代表', '代表', '委托（被代理）', '被委托（代理）'], ['审判长', '审判员'],
               ['住所地', '出生地', '户籍地'], ['出生日期', '判决日期'], ['性别', '民族', '机构社会编号', '律所', '律师执业证号']]

nodes_graph = load_graph.load_graph()

#mode 模式 by_step 查询与该节点n步距离内的所有节点，n由distance参数给出
# by_case 查询与该节点相关的案件，并且给出与该案件相关的所有节点
def query(id, mode = 'by_step', distance = 1):
    if not nodes_graph.has_key(id):
        return []

    worked_nodes = []
    working_nodes = [id]
    tmp_nodes = []
    result = []
    for mul in range(distance + 1):
        result.append([])
    info = nodes_graph[id]
    name = info[2]['name']

    result[0].append([id, name, info[3], '0'])
    if mode == 'by_step':
        for step in range(distance):
            #print step
            #print working_nodes
            #print worked_nodes
            #print nodes_graph
            #print step
            for node in working_nodes:
                #print working_nodes
                #print 'I worked in step ' + str(step)
                if node in worked_nodes:
                    #print "I continued"
                    continue

                info = nodes_graph[node]
                for i in info[3].items():
                    if i[0] in tmp_nodes or i[0] in working_nodes or i[0] in worked_nodes:
                        continue

                    '''
                    index = i[1].split('_')
                    fi = int(index[0])
                    si = int(index[1])
                    edge = edge_matrix[fi][si]
                    '''

                    features = nodes_graph[i[0]][2]
                        # print str(features).decode('unicode-escape')
                    if features.has_key('name'):
                        tmpname = features['name']
                    else:
                        tmpname = ''
                    name = ''
                    if type(tmpname) == list:
                        for j in tmpname:
                            name += j
                    else:
                        name = tmpname
                    # print name
                    result[step + 1].append([i[0], name, nodes_graph[i[0]][3], str(step + 1)])
                    #print str(result).decode('unicode-escape')

                    tmp_nodes.append(i[0])
            worked_nodes += working_nodes
            working_nodes = tmp_nodes
            tmp_nodes = []

    return result

def export_result(id, step, f):
    query_result = query(str(id), 'by_step', step)
    #print str(query_result).decode('unicode-escape')
    if not query_result == []:
        js = []

        #js['nodes'].append({"id": query_result[0][0], 'name': query_result[0][1],  'distance': query_result[0][3]})
        #source = query_result[0][0]

        for i in range(step + 1):
            #print i
            layer = query_result[i]
            if i < step:
                layer_next = query_result[i + 1]
            else:
                layer_next = []

            #print str(layer).decode('unicode-escape')
            #print str(layer_next).decode('unicode-escape') + '\n'
            for j in range(len(layer)):
                id = layer[j][0]
                name = layer[j][1]
                #js['nodes'].append({"id": id, 'name': layer[j][1], 'distance': layer[j][3]})
                #print id
                #print str(layer[j]).decode('unicode-escape')
                edges = layer[j][2]
                #print str(layer[j]).decode('unicode-escape')

                #print str(edges).decode('unicode-escape')

                for k in range(j + 1, len(layer)):
                    tar_id = layer[k][0]
                    tar_name = layer[k][1]
                    if edges.has_key(tar_id):
                        index = edges[tar_id].split('_')
                        js.append({"source": name, "target": tar_name, "rela": edge_matrix[int(index[0])][int(index[1])], "edge_color": int(index[0]), "type": 'resolved'})


                for l in range(len(layer_next)):
                    tar_id = layer_next[l][0]
                    tar_name = layer_next[l][1]
                    if edges.has_key(tar_id):
                        index = edges[tar_id].split('_')
                        js.append({"source": name, "target": tar_name, "rela": edge_matrix[int(index[0])][int(index[1])], "edge_color": int(index[0]), "type": 'resolved'})

        f.write(json.dumps(js, ensure_ascii=False).replace("\"source\"", 'source').replace("\"target\"", 'target').replace("\"rela\"", 'rela').replace("\"edge_color\"", 'edge_color').replace("\"type\"", 'type') + '\n')

o = open('search_result.txt', 'w')
export_result('25', 2, o)
