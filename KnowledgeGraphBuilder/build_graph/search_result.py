#coding=utf-8
import json
import sys
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

banned_classes = {'case': '0', 'loco': '1', 'time': '2', 'inst': '3', 'person': '4', 'lawyer': '5', 'lawfirm': '6', 'lawworker': '7', 'court': '8', 'attr': '9'}
inf = 5

nodes_graph = {}
nodes_map = {}

def load_graph(mode, args):
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
                    nodes_graph[j[0]] = j[1]
                del fj
                print 'Successfully loaded ' + i + '_graph'
    elif mode == '-':
        for i in files.keys():
            if i not in args:
                f = open(files[i], 'r')
                fj = json.load(f)
                f.close()
                for j in fj.items():
                    nodes_graph[j[0]] = j[1]
                del fj
                print 'Successfully loaded ' + i + '_graph'

#args: case, loco, time, person, inst, gender, ethic, social, lawyer, lawfirm, lawyernum, lawworker, court
def load_map(mode, args):
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
                    nodes_map[j[0]] = j[1]
                del fj
                print 'Successfully loaded ' + i + '_map'
    elif mode == '-':
        for i in files.keys():
            if i not in args:
                f = open(files[i], 'r')
                fj = json.load(f)
                f.close()
                for j in fj.items():
                    nodes_map[j[0]] = j[1]
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

load_graph('-', ['loco', 'time', 'gender', 'ethic', 'social', 'lawyernum', 'lawworker'])
print 'Successfully loaded all graphs'
load_map('-', ['loco', 'time', 'gender', 'ethic', 'social', 'lawyernum', 'lawworker'])
print 'Successfully loaded all maps'

# mode 模式 by_step 查询与该节点n步距离内的所有节点，n由distance参数给出
# by_case 查询与该节点相关的案件，并且给出与该案件相关的所有节点
# 默认不对地区（1），时间（2），法院（8），属性（9）做高于一次的跳转（即只能到达该节点，不得从该节点出发）
# 如果需要跳转，则要手动指定打开哪些跳转机制并且限定跳转涉及的节点数，即不能遍历所有节点
# 可以手动设置任何一种节点的最多遍历个数
# 案件（0），地区（1），时间（2），机构（3），当事人（4），律师（5），律所（6），法务（7），法院（8），属性（9）
# kwargs: case, loco, time, inst, person, lawyer, lawfirm, lawworker, court, attr
def query(id, mode = 'by_step', distance = 1, args = [], kwargs = {}):

    #print 'Successfully loaded all graphs'
    if not nodes_graph.has_key(id):
        return []
    #数字代表允许访问的节点个数
    # 案件（0），地区（1），时间（2），机构（3），当事人（4），律师（5），律所（6），法务（7），法院（8），属性（9）
    banned_nodes = {'0': inf, '1': 0, '2': 0, '3': inf, '4': inf, '5': inf, '6': 0, '7': 0, '8': 0, '9': 0}
    #根据用户开放的选项设置准许名单
    for item in kwargs.items():
        if banned_classes.has_key(item[0]):
            banned_nodes[banned_classes[item[0]]] = item[1]

    worked_nodes = []
    working_nodes = [id]
    tmp_nodes = []
    result = []
    for mul in range(distance + 1):
        result.append([])
    try:
        edges = nodes_graph[id]

        result[0].append([id, edges])
        if mode == 'by_step':
            for step in range(distance):
                #print step
                #print str(result).decode('unicode-escape')
                for node in working_nodes:
                    if node in worked_nodes:
                        continue

                    try:
                        edges = nodes_graph[node]
                        for i in edges.items():
                            if i[0] in tmp_nodes or i[0] in working_nodes or i[0] in worked_nodes:
                                continue

                            try:

                                index = i[0].split('_')[0]
                                if banned_nodes[index] > 0:
                                    tmp_nodes.append(i[0])
                                    banned_nodes[index] -= 1
                                    result[step + 1].append([i[0], nodes_graph[i[0]]])
                                else:
                                    result[step + 1].append([i[0], {}])

                            except:
                                pass
                    except:
                        pass
                worked_nodes += working_nodes
                working_nodes = tmp_nodes
                tmp_nodes = []
                print step
            print 'out of step'
        print 'out of if'
    except:
        pass

    print 'out of try'

    #del nodes_graph

    print str(result).decode('unicode-escape')
    return result

#对于内存有限的机器，采用流式搜索，即不永久存储graph，先求出节点，然后释放内存，再去map中找info
#对于内存充足的机器，采用持续载入Graph和Map的方法
def flow_search_result(id, mode, step, f, *args, **kwargs):
    query_result = query(str(id), mode, step, args, kwargs)
    #pdb.set_trace()
    print 'Search finished. Now constructing graph...'
    #nodes_map = {}
    #load_graph.load_map(nodes_map, '-', args)
    print 'Successfully loaded all maps'
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
                try:
                    name = load_graph.get_name(id, nodes_map)
                    print name
                #js['nodes'].append({"id": id, 'name': layer[j][1], 'distance': layer[j][3]})
                #print id
                #print str(layer[j]).decode('unicode-escape')
                    edges = layer[j][1]
                #print str(layer[j]).decode('unicode-escape')

                #print str(edges).decode('unicode-escape')

                    for k in range(j + 1, len(layer)):
                        tar_id = layer[k][0]
                        try:
                            tar_name = load_graph.get_name(tar_id, nodes_map)
                            print tar_name
                            if edges.has_key(tar_id):
                                index = edges[tar_id].split('_')
                                js.append({"source": name, "target": tar_name, "rela": edge_matrix[int(index[0])][int(index[1])], "edge_color": int(index[0]), "type": 'resolved'})
                        except:
                            pass

                    for l in range(len(layer_next)):
                        tar_id = layer_next[l][0]
                        try:
                            tar_name = load_graph.get_name(tar_id, nodes_map)
                            print tar_name
                            if edges.has_key(tar_id):
                                index = edges[tar_id].split('_')
                                js.append({"source": name, "target": tar_name, "rela": edge_matrix[int(index[0])][int(index[1])], "edge_color": int(index[0]), "type": 'resolved'})
                        except:
                            pass
                except:
                    pass

        f.write(json.dumps(js, ensure_ascii=False).replace("\"source\"", 'source').replace("\"target\"", 'target').replace("\"rela\"", 'rela').replace("\"edge_color\"", 'edge_color').replace("\"type\"", 'type') + '\n')

#args: case, loco, time, person, inst, gender, ethic, social, lawyer, lawfirm, lawyernum, lawworker, court
o = open('search_result.txt', 'w')
print 'start debugging...'
#pdb.set_trace()
flow_search_result('3_451', "by_step", 2, o, 'loco', 'time', 'gender', 'ethic', 'social', 'lawyernum', 'lawworker')
