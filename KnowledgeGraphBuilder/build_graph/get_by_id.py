#coding=utf-8
import json
import sys
import load_graph
reload(sys)
sys.setdefaultencoding('utf-8')

nodes_map = {}

load_graph.load_map(nodes_map, '-', ['loco', 'time', 'gender', 'ethic', 'social', 'lawyernum', 'lawworker'])

while(True):
    id = raw_input()
    print load_graph.get_name(id, nodes_map)
