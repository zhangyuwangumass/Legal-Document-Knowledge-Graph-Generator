#coding=utf-8

#ids模块负责将json文件中的各实体间依赖关系写入不同文件中。
#实体分为10类：案件（0），地区（1），时间（2），机构（3），当事人（4），辩护人（5）， 代理律师（6），律所（7），法务（8），法院（9）
#实体唯一标识码以 '前缀_id' 的形式表示。
#实体的额外特征（features）以attributes的形式存储在id后的字典里
#实体间的关系以 '关系类别_关系参数' 的形式表示。关系类别分为9类：
#关系      代号    参数
#相等关系   0      0~1，概率
#当事关系   1      0 原告 1被告 2 律师 3 代表人 4 代理人 5 审判长 6 审判员 7 法院
#诉讼关系   2      0 被诉 1 起诉
#辩护关系   3      0 被辩护 1 辩护
#代表关系   4      0 被代表 1 代表 2 委托（被代理） 3 被委托（代理）
#法院关系   5      0 审判长 1 审判员
#地点关系   6      0 住所地 1 出生地 2 户籍地
#时间关系   7      0 出生日期 1 判决日期
#属性关系   8      0 性别 1 民族 2 机构社会编号 3 律所 4 律师执业证号
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

case_map = {}
court_map = {}

case_dict = {}
court_dict = {}
loco_dict = {}
time_dict = {}
inst_dict = {}
gender_dict ={}
ethic_dict = {}
social_dict = {}
lawfirm_dict = {}
lawyernum_dict = {}

def dict_to_line(p, case_id):
	if p.has_key("性别".decode('utf-8')):
		pline = [[case_id], (str(p['id'])).decode('utf-8'), {}, {case_id: '1_0'}]
		pline[2]['type'.decode('utf-8')] = 'p'
		if p["姓名".decode('utf-8')] != []:
			name = ''
			for i in p["姓名".decode('utf-8')]:
				name += i
			pline[2]['name'.decode('utf-8')] = name
		sex = p["性别".decode('utf-8')]
		if sex != []:
			if gender_dict.has_key(sex[0]):
				gender_dict[sex[0]][3][str(p['id'])] = '8_0'
			else:
				gender_dict[sex[0]] = [[case_id], sex[0], {'name': sex[0]}, {str(p['id']): '8_0'}]
			pline[3][sex[0]] = '8_0'
			#pline[2]['sex'.decode('utf-8')] = p["性别".decode('utf-8')][0]
		pr = p["户籍".decode('utf-8')]
		if p["户籍".decode('utf-8')] != []:
			#register = ''
			#for i in p["户籍".decode('utf-8')]:
			#	register += i
			#pline[2]['register'.decode('utf-8')] = register
			if loco_dict.has_key(pr[0]):
				loco_dict[pr[0]][3][str(p['id'])] = '6_2'
			else:
				loco_dict[pr[0]] = [[case_id], pr[0], {'name': pr[0]}, {str(p['id']): '6_2'}]
			pline[3][pr[0]] = '6_2'
			#pline[2]['register'.decode('utf-8')] = pr
		bir = p["出生年份".decode('utf-8')]
		if bir != []:
			if time_dict.has_key(bir[0]):
				time_dict[bir[0]][3][str(p['id'])] = '7_0'
			else:
				time_dict[bir[0]] = [[case_id], bir[0], {'name': bir[0]}, {str(p['id']): '7_0'}]
			pline[3][bir[0]] = '7_0'
			#pline[2]['birthday'.decode('utf-8')] = bir[0]
		birp = p["出生地".decode('utf-8')]
		if birp != []:
			#birthplace = ''
			#for i in p["出生地".decode('utf-8')]:
			#	birthplace += i
			#pline[2]['birthplace'.decode('utf-8')] = birthplace
			if loco_dict.has_key(birp[0]):
				loco_dict[birp[0]][3][str(p['id'])] = '6_1'
			else:
				loco_dict[birp[0]] = [[case_id], birp[0], {'name': birp[0]}, {str(p['id']): '6_1'}]
			pline[3][birp[0]] = '6_1'
			#pline[2]['birthplace'.decode('utf-8')] = birp
		ethic = p["民族".decode('utf-8')]
		if ethic != []:
			if ethic_dict.has_key(ethic[0]):
				ethic_dict[ethic[0]][3][str(p['id'])] = '8_1'
			else:
				ethic_dict[ethic[0]] = [[case_id], ethic[0], {'name': ethic[0]}, {str(p['id']): '8_1'}]
			pline[3][ethic[0]] = '8_1'
			#pline[2]['ethic'.decode('utf-8')] = p['民族'.decode('utf-8')][0]
	else:
		pline = [[case_id], (str(p['id'])).decode('utf-8'), {}, {case_id: '1_0'}]
		pline[2]['type'.decode('utf-8')] = 'i'
		#如果名称中的关键词在已有词典中都存在，则采用已有的id
		if p["姓名".decode('utf-8')] != []:
			#name = ''
			#for i in p["姓名".decode('utf-8')]:
			#	name += i
			#pline[2]['name'.decode('utf-8')] = name
			pline[2]['name'.decode('utf-8')] = p["姓名".decode('utf-8')]
		reg = p["住所地".decode('utf-8')]
		if reg != []:
			#register = ''
			#for i in p["住所地".decode('utf-8')]:
			#	register += i
			#pline[2]['register'.decode('utf-8')] = register
			if loco_dict.has_key(reg[0]):
				loco_dict[reg[0]][3][str(p['id'])] = '6_0'
			else:
				loco_dict[reg[0]] = [[case_id], reg[0], {'name': reg[0]}, {str(p['id']): '6_0'}]
			pline[3][reg[0]] = '6_0'
		social = p["社会代码".decode('utf-8')]
		if social != '' and social != []:
			if social_dict.has_key(social):
				social_dict[social][3][str(p['id'])] = '8_2'
			else:
				social_dict[social] = [[case_id], social, {'name': social}, {str(p['id']): '8_2'}]
			pline[3][social] = '8_2'
			#pline[2]['social_num'.decode('utf-8')] = p["社会代码".decode('utf-8')]

	return pline

def lawyer_to_line(p, case_id):
	pline = [[case_id], str(p['id']), {}, {case_id: '1_2'}]
	if p["姓名".decode('utf-8')] != []:
		name = ''
		for i in p["姓名".decode('utf-8')]:
			name += i
		pline[2]['name'] = name
	lawfirm = p["事务所及职位".decode('utf-8')]
	if lawfirm != []:
		firm = ''
		for i in lawfirm:
			if i != '事务所':
				firm += i
			else:
				firm += i
				break
		if lawfirm_dict.has_key(firm):
			lawfirm_dict[firm][3][str(p['id'])] = '8_3'
		else:
			lawfirm_dict[firm] = [[case_id], firm, {'name': firm}, {str(p['id']): '8_3'}]
		pline[3][firm] = '8_3'
		#pline[2]['firm'] = firm
	reg = p["地区".decode('utf-8')]
	if reg != []:
		#register = ''
		#for i in p["地区".decode('utf-8')]:
		#	register += i
		#pline[2]['register'] = register
		if loco_dict.has_key(reg[0]):
			loco_dict[reg[0]][3][str(p['id'])] = '6_0'
		else:
			loco_dict[reg[0]] = [[case_id], reg[0], {'name': reg[0]}, {str(p['id']): '6_0'}]
		pline[3][reg[0]] = '6_0'
		#pline[2]['register'] = reg
	lawyernum = p["执业证号".decode('utf-8')]
	if lawyernum != '' and lawyernum != []:
		if lawyernum_dict.has_key(lawyernum[0]):
			lawyernum_dict[lawyernum][3][str(p['id'])] = '8_4'
		else:
			lawyernum_dict[lawyernum] = [[case_id], lawyernum, {'name': lawyernum}, {str(p['id']): '8_4'}]
		pline[3][lawyernum] = '8_4'
		#pline[2]['social_num'] = p["执业证号".decode('utf-8')][0]

	return pline

def repre_to_line(p, case_id):
	pline = [[case_id], str(p['id']), {}, {case_id: '1_3'}]
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
	pline = [[case_id], str(p['id']), {}, {case_id: '1_4'}]
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
		pr = p["户籍".decode('utf-8')]
		if p["户籍".decode('utf-8')] != []:
			# register = ''
			# for i in p["户籍".decode('utf-8')]:
			#	register += i
			# pline[2]['register'.decode('utf-8')] = register
			if loco_dict.has_key(pr[0]):
				loco_dict[pr[0]][3][str(p['id'])] = '6_2'
			else:
				loco_dict[pr[0]] = [[case_id], pr[0], {'name': pr[0]}, {str(p['id']): '6_2'}]
			pline[3][pr[0]] = '6_2'
			#pline[2]['register'.decode('utf-8')] = pr
		bir = p["出生年份".decode('utf-8')]
		if bir != []:
			if time_dict.has_key(bir[0]):
				time_dict[bir[0]][3][str(p['id'])] = '7_0'
			else:
				time_dict[bir[0]] = [[case_id], bir[0], {'name': bir[0]}, {str(p['id']): '7_0'}]
			pline[3][bir[0]] = '7_0'
		birp = p["出生地".decode('utf-8')]
		if birp != []:
			# birthplace = ''
			# for i in p["出生地".decode('utf-8')]:
			#	birthplace += i
			# pline[2]['birthplace'.decode('utf-8')] = birthplace
			if loco_dict.has_key(birp[0]):
				loco_dict[birp[0]][3][str(p['id'])] = '6_1'
			else:
				loco_dict[birp[0]] = [[case_id], birp[0], {'name': birp[0]}, {str(p['id']): '6_1'}]
			pline[3][birp[0]] = '6_1'
			#pline[2]['birthplace'.decode('utf-8')] = birp
		ethic = p["民族".decode('utf-8')]
		if ethic != []:
			if ethic_dict.has_key(ethic[0]):
				ethic_dict[ethic[0]][3][str(p['id'])] = '8_1'
			else:
				ethic_dict[ethic[0]] = [[case_id], ethic[0], {'name': ethic[0]}, {str(p['id']): '8_1'}]
			pline[3][ethic[0]] = '8_1'

	return pline

def build_graph_from_json(json, p_f, i_f, case_id, court_id):

	court = json['法院'.decode('utf-8')]
	case = json['文书编号'.decode('utf-8')]
	#type = json['文书类型'.decode('utf-8')]
	prosecu = json['原告'.decode('utf-8')]
	defend = json['被告'.decode('utf-8')]
	advocate = json['辩护人'.decode('utf-8')]
	lawyer = json['代理律师'.decode('utf-8')]
	law_worker = json['法务人员'.decode('utf-8')]
	represen = json['法定代表人'.decode('utf-8')]
	trustee = json['委托代理人'.decode('utf-8')]

	case_increment = False
	court_increment = False

	cur_case_id = ''
    #第一步：为案件赋id
	case_line = [[], '', {}, {}]
	if case != '':
		if case_map.has_key(case):
			cur_case_id = case_map[case]
			case_line[0].append(cur_case_id)
			case_line[1] = cur_case_id
			case_line[2]['name'] = case
		else:
			cur_case_id = '0_' + str(case_id)
			case_map[case] = cur_case_id
			case_line[0].append(cur_case_id)
			case_line[1] = cur_case_id
			case_line[2]['name'] = case
			case_increment = True

	if not case_dict.has_key(cur_case_id):
		case_dict[cur_case_id] = case_line

	# 法院关系   5      0 审判长 1 审判员
	#第二步：检索法院，如果已存在，则直接赋已有的id，否则向字典中加入新的法院
	cur_court_id = ''
	court_line = [[], '', {}, {}]
	if court != '':
		if court_map.has_key(court):
			cur_court_id = court_map[court]
			court_line = court_dict[cur_court_id]
			court_line[0].append(cur_case_id)
			court_line[3][cur_case_id] = '1_7'
		else:
			cur_court_id = '9_' + str(court_id)
			court_map[court] = '9_' + str(court_id)
			court_line = [[cur_case_id], cur_court_id, {'name': court}, {cur_case_id: '1_7'}]
			court_increment = True
		case_dict[cur_case_id][3][cur_court_id] = '1_7'

	if not court_dict.has_key(cur_court_id):
		court_dict[cur_court_id] = court_line

	# 法院关系   5      0 审判长 1 审判员
	#第三步：建立法务人员与法院的关系
	for item in law_worker:
		posi = item['职务'.decode('utf-8')][0]
		na = item['姓名'.decode('utf-8')][0]
		if posi == '审判长':
			if cur_court_id != '':
				p_f.write(js.dumps([[cur_case_id], str(item['id']), {'name': na}, {cur_court_id: '5_0', cur_case_id: '1_5'}], ensure_ascii=False) + '\n')
			else:
				p_f.write(js.dumps([[cur_case_id], str(item['id']), {'name': na}, {cur_case_id: '1_5'}],
								   ensure_ascii=False) + '\n')
			case_dict[cur_case_id][3][str(item['id'])] = '1_5'
			court_dict[cur_court_id][3][str(item['id'])] = '5_0'
		elif posi == '审判员':
			if cur_court_id != '':
				p_f.write(js.dumps([[cur_case_id], str(item['id']), {'name': na}, {cur_court_id: '5_1', cur_case_id: '1_6'}],
								   ensure_ascii=False) + '\n')
			else:
				p_f.write(js.dumps([[cur_case_id], str(item['id']), {'name': na}, {cur_case_id: '1_6'}],
								   ensure_ascii=False) + '\n')
			case_dict[cur_case_id][3][str(item['id'])] = '1_6'
			court_dict[cur_court_id][3][str(item['id'])] = '5_1'

	#第三步：建立当事人、当事机构和律师之间的关系
	person_dict = {}
	advocate_dict = {}
	lawyer_dict = {}

	for p in prosecu:
		pline = dict_to_line(p, cur_case_id)
		pline[2]['prosecu'] = '1'
		for d in defend:
			dline = dict_to_line(d, cur_case_id)
			pline[3][dline[1]] = '2_1'
		person_dict[p['id']] = pline
		case_dict[cur_case_id][3][p['id']] = '1_0'

	for d in defend:
		dline = dict_to_line(d, cur_case_id)
		dline[2]['prosecu'] = '0'
		for p in prosecu:
			pline = dict_to_line(p, cur_case_id)
			dline[3][pline[1]] = '2_0'
		person_dict[d['id']] = dline
		case_dict[cur_case_id][3][d['id']] = '1_1'

	for a in advocate:
		aline = lawyer_to_line(a, cur_case_id)
		id = a['代理方id'.decode('utf-8')]
		if person_dict.has_key(id):
			person_dict[id][3][aline[1]] = '3_0'
			aline[3][id] = '3_1'
			advocate_dict[a['id']] = aline
		case_dict[cur_case_id][3][a['id']] = '1_2'

	for l in lawyer:
		lline = lawyer_to_line(l, cur_case_id)
		id = l['代理方id'.decode('utf-8')]
		if person_dict.has_key(id):
			person_dict[id][3][lline[1]] = '4_2'
			lline[3][id] = '4_3'
			lawyer_dict[l['id']] = lline
		case_dict[cur_case_id][3][l['id']] = '1_3'

	for r in represen:
		rline = repre_to_line(r, cur_case_id)
		id = r['代理方id'.decode('utf-8')]
		if person_dict.has_key(id):
			person_dict[id][3][rline[1]] = '4_0'
			rline[3][id] = '4_1'
			person_dict[r['id']] = rline
		case_dict[cur_case_id][3][r['id']] = '1_3'

	for t in trustee:
		tline = tru_to_line(t, cur_case_id)
		id = t['代理方id'.decode('utf-8')]
		if person_dict.has_key(id):
			person_dict[id][3][tline[1]] = '4_2'
			tline[3][id] = '4_3'
			person_dict[t['id']] = tline
		case_dict[cur_case_id][3][t['id']] = '1_4'

	#第四步 建立当前所有人与案件本身的关系


	#第五步：打印输出
	#f.write(js.dumps(case_line, ensure_ascii=False) + '\n')

	for i in person_dict.values():
		if i[2]['type'] == 'p':
			if i[2].has_key('type'):
				i[2].pop('type')
			if i[2].has_key('prosecu'):
				i[2].pop('prosecu')
			p_f.write(js.dumps(i, ensure_ascii=False) + '\n')
		else:
			if i[2].has_key('type'):
				i[2].pop('type')
			if i[2].has_key('prosecu'):
				i[2].pop('prosecu')
			i_f.write(js.dumps(i, ensure_ascii=False) + '\n')

	for i in advocate_dict.values():
		p_f.write(js.dumps(i, ensure_ascii=False) + '\n')

	for i in lawyer_dict.values():
		p_f.write(js.dumps(i, ensure_ascii=False) + '\n')

	if case_increment:
		case_id += 1
	if court_increment:
		court_id += 1
	return case_id, court_id

f = open('content_json_sample.txt', 'r')

p_graph = open('person_graph.txt', 'w')
i_graph = open('institute_graph.txt', 'w')
loco_graph = open('loco_graph.txt', 'w')
time_graph = open('time_graph.txt', 'w')
gender_graph = open('gender_graph.txt', 'w')
ethic_graph = open('ethic_graph.txt', 'w')
social_graph = open('social_graph.txt', 'w')
lawfirm_graph = open('lawfirm_graph.txt', 'w')
lawyernum_graph = open('lawyernum_graph.txt', 'w')
case_graph = open('case_graph.txt', 'w')
court_graph = open('court_graph.txt', 'w')

f_case_map = open('case_map.txt', 'w')
f_court_map = open('court_map.txt', 'w')

case_id = 0
court_id = 0

for l in f:
	if l != '\n':
		json = js.loads(l)
		case_id, court_id = build_graph_from_json(json, p_graph, i_graph, case_id, court_id)
'''
for i in loco_dict.items():
	loco_graph.write(js.dumps(i, ensure_ascii=False) + '\n')

for i in time_dict.items():
	time_graph.write(js.dumps(i, ensure_ascii=False) + '\n')

for i in case_dict.items():
	f_case_map.write(js.dumps(i, ensure_ascii=False) + '\n')

for i in court_dict.items():
	f_court_map.write(js.dumps(i, ensure_ascii=False) + '\n')
'''

loco_graph.write(js.dumps(loco_dict, ensure_ascii=False) + '\n')

time_graph.write(js.dumps(time_dict, ensure_ascii=False) + '\n')

gender_graph.write(js.dumps(gender_dict, ensure_ascii=False) + '\n')

ethic_graph.write(js.dumps(ethic_dict, ensure_ascii=False) + '\n')

social_graph.write(js.dumps(social_dict, ensure_ascii=False) + '\n')

lawfirm_graph.write(js.dumps(lawfirm_dict, ensure_ascii=False) + '\n')

lawyernum_graph.write(js.dumps(lawyernum_dict, ensure_ascii=False) + '\n')

case_graph.write(js.dumps(case_dict, ensure_ascii=False) + '\n')

court_graph.write(js.dumps(court_dict, ensure_ascii=False) + '\n')

#从案件编号映射到案件id
f_case_map.write(js.dumps(case_map, ensure_ascii=False) + '\n')
#从法院名称映射到法院id
f_court_map.write(js.dumps(court_map, ensure_ascii=False) + '\n')