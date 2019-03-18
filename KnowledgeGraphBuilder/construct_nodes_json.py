#coding=utf-8
import json

js = {"nodes": [], "links": []}

f = open('0.txt', 'r')

for l in f:
    lj = json.loads(l)
    js["nodes"].append({"id": lj[0], "group": "0"})

for k in range(3, 7):
    f = open(str(k) + '.txt', 'r')

    for l in f:
        lj = json.loads(l)
        js["nodes"].append({"id": lj[1], "group": "3"})
        js["links"].append({"source": lj[0][0], "target": lj[1], "value": 1})
        js["links"].append({"source": lj[1], "target": lj[0][0], "value": 1})
        for i in lj[3].keys():
            js["links"].append({"source": lj[1], "target": i, "value": 1})

o = open('nodes_reduced.json', 'w')
o.write(json.dumps(js, ensure_ascii=False))
