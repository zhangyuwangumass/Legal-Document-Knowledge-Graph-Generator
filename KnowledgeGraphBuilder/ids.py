#coding=utf-8

#ids模块负责将json文件中的各实体间依赖关系写入不同文件中。
#实体分为10类：案件（0），地区（1），时间（2），机构（3），当事人（4），辩护人（5）， 代理律师（6），律所（7），法务（8），法院（9）
#实体唯一标识码以 '前缀_id' 的形式表示。
#实体的额外特征（features）以attributes的形式存储在id后的字典里
#实体间的关系以 '关系类别_关系参数' 的形式表示。关系类别分为9类：
#关系      代号    参数
#相等关系   0      0~1，概率
#当事关系   1      0 原告 1 被告 2 公诉机关 3 法院 4 律师 5 代理人 6 法务人员
#诉讼关系   2      0 被诉 1 起诉
#辩护关系   3      0 被辩护 1 辩护
#代表关系   4      0 被代表 1 代表 2 被委托（代理） 3 委托（代理）
#例：['123', '4_12466', {'name':'李四','sex':'m','id_num':'1234567890'}, {'3_24588':'2_1', '5_90331':'3_0'}]，代表
#在文书123中，名为李四，身份证号为1234567890的男性当事人12466起诉了机构24588，并请了律师90331为自己辩护

#json格式：
#{"文书类型": "民事判决书\n", "辩护人": [], "被告": [{"出生年份": ["1982年"], "性别": ["女"], "户籍": [], "代理方id": -1,
#  "民族": ["汉族"], "id": 85, "出生地": [], "姓名": ["孙艳"]}], "文书编号": "（2015）新中民金终字第412号\n",
# "原告": [{"社会代码": [], "住所地": ["新乡市", "金穗", "大道", "111号"], "id": 82,
# "姓名": ["中国", "平安", "财产", "保险", "股份", "有限公司", "新乡", "中心", "支公司"]}],
#  "法定代表人": [{"职务": ["经理"], "代理方id": 82, "id": 83, "姓名": ["刘瑛"]}],
# "法院": "河南省新乡市中级人民法院\n", "法务人员": [{"职务": ["审判长"], "id": 87, "姓名": ["张立东"]},
# {"职务": ["审判员"], "id": 88, "姓名": ["王师斌"]}, {"职务": ["审判员"], "id": 89, "姓名": ["宋筱"]},
# {"职务": ["书记员"], "id": 90, "姓名": ["刘林琦"]}], "委托代理人": [{"代理方id": 82, "事务所及职位": ["牧野", "律师", "事务所", "律师"],
#  "执业证号": [], "id": 84, "地区": ["河南"], "姓名": ["朱占文", "郜红"]},
# {"代理方id": 85, "事务所及职位": ["龙健", "律师", "事务所", "律师"], "执业证号": [],
# "id": 86, "地区": ["河南"], "姓名": ["李艳霞"]}]}
#dict = {'法院': '', '公诉机关': '', '文书类型': '', '文书编号': '', '原告': [], '被告':[], '辩护人': [],
# '法务人员': [], '法定代表人': [],'委托代理人': []}

import sys
import json as js
reload(sys)
sys.setdefaultencoding( "utf-8" )

keys = ['法院', '公诉机关', '文书类型', '文书编号', '原告', '被告', '辩护人', '法务人员', '法定代表人','委托代理人']

loco_dict = {}
time_dict = {}
case_dict = {}
court_dict = {}

def dict_to_line(p, case_id):
	if p.has_key("性别".decode('utf-8')):
		pline = [[case_id], ('4_' + str(p['id'])).decode('utf-8'), {}, {}]
		pline[2]['type'.decode('utf-8')] = 'p'
		if p["姓名".decode('utf-8')] != []:
			name = ''
			for i in p["姓名".decode('utf-8')]:
				name += i
			pline[2]['name'.decode('utf-8')] = name
		if p["性别".decode('utf-8')] != []:
			pline[2]['sex'.decode('utf-8')] = p["性别".decode('utf-8')][0]
		if p["户籍".decode('utf-8')] != []:
			register = ''
			for i in p["户籍".decode('utf-8')]:
				register += i
			pline[2]['register'.decode('utf-8')] = register
		if p["出生年份".decode('utf-8')] != []:
			pline[2]['birthday'.decode('utf-8')] = p["出生年份".decode('utf-8')][0]
		if p["出生地".decode('utf-8')] != []:
			birthplace = ''
			for i in p["出生地".decode('utf-8')]:
				birthplace += i
			pline[2]['birthplace'.decode('utf-8')] = birthplace
		if p["民族".decode('utf-8')] != []:
			pline[2]['ethic'.decode('utf-8')] = p['民族'.decode('utf-8')][0]
	else:
		pline = [[case_id], ('3_' + str(p['id'])).decode('utf-8'), {}, {}]
		pline[2]['type'.decode('utf-8')] = 'i'
		if p["姓名".decode('utf-8')] != []:
			name = ''
			for i in p["姓名".decode('utf-8')]:
				name += i
			pline[2]['name'.decode('utf-8')] = name
		if p["住所地".decode('utf-8')] != []:
			register = ''
			for i in p["住所地".decode('utf-8')]:
				register += i
			pline[2]['register'.decode('utf-8')] = register
		if p["社会代码".decode('utf-8')] != []:
			pline[2]['social_num'.decode('utf-8')] = p["社会代码".decode('utf-8')]

	return pline

def lawyer_to_line(p, pref, case_id):
	pline = [[case_id], pref + '_' + str(p['id']), {}, {}]
	if p["姓名".decode('utf-8')] != []:
		name = ''
		for i in p["姓名".decode('utf-8')]:
			name += i
		pline[2]['name'] = name
	if p["事务所及职位".decode('utf-8')] != []:
		firm = ''
		for i in p["事务所及职位".decode('utf-8')]:
			firm += i
		pline[2]['firm'] = firm
	if p["地区".decode('utf-8')] != []:
		register = ''
		for i in p["地区".decode('utf-8')]:
			register += i
		pline[2]['register'] = register
	if p["执业证号".decode('utf-8')] != []:
		pline[2]['social_num'] = p["执业证号".decode('utf-8')][0]

	return pline

def repre_to_line(p, case_id):
	pline = [[case_id], '4_' + str(p['id']), {}, {}]
	pline[2]['type'] = 'p'
	if p["姓名".decode('utf-8')] != []:
		name = ''
		for i in p["姓名".decode('utf-8')]:
			name += i
		pline[2]['name'] = name
	if p["职务".decode('utf-8')] != []:
		job = ''
		for i in p["职务".decode('utf-8')]:
			job += i
		pline[2]['job'] = job

	return pline

def tru_to_line(p, case_id):
	pline = [[case_id], '4_' + str(p['id']), {}, {}]
	pline[2]['type'] = 'p'
	if p.has_key("职务".decode('utf-8')):
		if p["姓名".decode('utf-8')] != []:
			name = ''
			for i in p["姓名".decode('utf-8')]:
				name += i
			pline[2]['name'] = name
		if p["职务".decode('utf-8')] != []:
			job = ''
			for i in p["职务".decode('utf-8')]:
				job += i
			pline[2]['job'] = job
	else:
		pline[2]['type'] = 'p'
		if p["姓名".decode('utf-8')] != []:
			name = ''
			for i in p["姓名".decode('utf-8')]:
				name += i
			pline[2]['name'] = name
		if p["性别".decode('utf-8')] != []:
			pline[2]['sex'] = p["性别".decode('utf-8')][0]
		if p["户籍".decode('utf-8')] != []:
			register = ''
			for i in p["户籍".decode('utf-8')]:
				register += i
			pline[2]['register'] = register
		if p["出生年份".decode('utf-8')] != []:
			pline[2]['birthday'] = p["出生年份".decode('utf-8')][0]
		if p["出生地".decode('utf-8')] != []:
			birthplace = ''
			for i in p["出生地".decode('utf-8')]:
				birthplace += i
			pline[2]['birthplace'] = birthplace
		if p["民族".decode('utf-8')] != []:
			pline[2]['ethic'] = p['民族'.decode('utf-8')][0]

	return pline

def build_graph_from_json(json, f0, f3, f4, f5, f6, f9, case_id, court_id, loco_id = 0, time_id = 0, lawfirm_id = 0):

	court = json['法院'.decode('utf-8')]
	case = json['文书编号'.decode('utf-8')]
	type = json['文书类型'.decode('utf-8')]
	prosecu = json['原告'.decode('utf-8')]
	defend = json['被告'.decode('utf-8')]
	advocate = json['辩护人'.decode('utf-8')]
	lawyer = json['代理律师'.decode('utf-8')]
	law_worker = json['法务人员'.decode('utf-8')]
	represen = json['法定代表人'.decode('utf-8')]
	trustee = json['委托代理人'.decode('utf-8')]

	case_increment = False
	court_increment = False

    #第一步：为案件赋id
	if case != '':
		case_line = ['', '']
		if case_dict.has_key(case):
			case_line[0] = str(case_dict[case])
		else:
			case_dict[case] = case_id
			case_line[0] = str(case_id)
			case_line[1] = case
			case_increment = True
	#第二步：检索法院，如果已存在，则直接赋已有的id，否则向字典中加入新的法院
	if court != '':
		court_line = [str(case_id), '', []]

		if court_dict.has_key(court):
			court_line[1] = court_dict[court]
		else:
			court_dict[court] = '9_' + str(court_id)
			court_line[1] = '9_' + str(court_id)
			court_line[2] = law_worker
			court_increment = True

	#第三步：建立当事人、当事机构和律师之间的关系
	person_dict = {}
	advocate_dict = {}
	lawyer_dict = {}

	for p in prosecu:
		pline = dict_to_line(p, str(case_id))
		pline[2]['prosecu'] = '1'
		for d in defend:
			dline = dict_to_line(d, str(case_id))
			pline[3][dline[1]] = '2_1'
		person_dict[p['id']] = pline

	for d in defend:
		dline = dict_to_line(d, str(case_id))
		dline[2]['prosecu'] = '0'
		for p in prosecu:
			pline = dict_to_line(p, str(case_id))
			dline[3][pline[1]] = '2_0'
		person_dict[d['id']] = dline

	for a in advocate:
		aline = lawyer_to_line(a, '5', str(case_id))
		id = a['代理方id'.decode('utf-8')]
		person_dict[id][3][aline[1]] = '3_0'
		aline[3][person_dict[id][1]] = '3_1'
		advocate_dict[a['id']] = aline

	for l in lawyer:
		lline = lawyer_to_line(l, '6', str(case_id))
		id = l['代理方id'.decode('utf-8')]
		person_dict[id][3][lline[1]] = '4_2'
		lline[3][person_dict[id][1]] = '4_3'
		lawyer_dict[l['id']] = lline

	for r in represen:
		rline = repre_to_line(r, str(case_id))
		id = r['代理方id'.decode('utf-8')]
		person_dict[id][3][rline[1]] = '4_0'
		rline[3][person_dict[id][1]] = '4_1'
		person_dict[r['id']] = rline

	for t in trustee:
		tline = tru_to_line(t, str(case_id))
		id = t['代理方id'.decode('utf-8')]
		person_dict[id][3][tline[1]] = '4_2'
		tline[3][person_dict[id][1]] = '4_3'
		person_dict[t['id']] = tline

	#第四步 建立当前所有人与案件本身的关系


	#第五步：打印输出
	f0.write(js.dumps(case_line, ensure_ascii=False) + '\n')

	for i in person_dict.values():
		if i[2]['type'] == 'p':
			if i[2].has_key('type'):
				i[2].pop('type')
			if i[2].has_key('prosecu'):
				i[2].pop('prosecu')
			f4.write(js.dumps(i, ensure_ascii=False) + '\n')
		else:
			if i[2].has_key('type'):
				i[2].pop('type')
			if i[2].has_key('prosecu'):
				i[2].pop('prosecu')
			f3.write(js.dumps(i, ensure_ascii=False) + '\n')

	for i in advocate_dict.values():
		f5.write(js.dumps(i, ensure_ascii=False) + '\n')

	for i in lawyer_dict.values():
		f6.write(js.dumps(i, ensure_ascii=False) + '\n')

	try:
		f9.write(js.dumps(court_line, ensure_ascii=False) + '\n')
	except:
		pass

	if case_increment:
		case_id += 1
	if court_increment:
		court_id += 1
	return case_id, court_id

f = open('content_json_sample.txt', 'r')

f0 = open('0.txt', 'w')
f3 = open('3.txt', 'w')
f4 = open('4.txt', 'w')
f5 = open('5.txt', 'w')
f6 = open('6.txt', 'w')
f9 = open('9.txt', 'w')

f_case_map = open('case_map.txt', 'w')
f_court_map = open('court_map.txt', 'w')

case_id = 0
court_id = 0

for l in f:
	if l != '\n':
		json = js.loads(l)
		case_id, court_id = build_graph_from_json(json, f0, f3, f4, f5, f6, f9, case_id, court_id)

for i in case_dict.items():
	f_case_map.write(js.dumps(i, ensure_ascii=False) + '\n')

for i in court_dict.items():
	f_court_map.write(js.dumps(i, ensure_ascii=False) + '\n')