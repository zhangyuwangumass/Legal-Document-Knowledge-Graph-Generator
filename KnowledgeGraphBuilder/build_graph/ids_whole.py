#coding=utf-8

#ids模块负责将json文件中的各实体间依赖关系写入不同文件中。
#实体分为10类：案件（0），地区（1），时间（2），机构（3），当事人（4），律师（5），律所（6），法务（7），法院（8），属性（9）
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

#需要给所有实体赋唯一id
#id前缀：
#案件（0），地区（1），时间（2），机构（3），当事人（4），律师（5），律所（6），法务（7），法院（8），属性（9）
#map是用于将id值映射到其属性
case_map = {}      #0
loco_map = {}      #1
time_map = {}      #2
inst_map = {}      #3
person_map = {}    #4
lawyer_map = {}    #5
gender_map = {}
ethic_map = {}
social_map = {}
lawfirm_map = {}   #6
lawworker_map = {} #7
lawyernum_map = {}
court_map = {}     #8

#dict是用于存储id的边关系，便于按类查找
case_dict = {}
loco_dict = {}
time_dict = {}
inst_dict = {}
person_dict = {}
lawyer_dict = {}
gender_dict ={}
ethic_dict = {}
social_dict = {}
lawfirm_dict = {}
lawworker_dict = {}
lawyernum_dict = {}
court_dict = {}


#[id, {属性}]
def dict_to_line(p, case_id, loco_id, time_id, lawfirm_id, attr_id):
	if p["姓名".decode('utf-8')] != []:
		name = ''
		for i in p["姓名".decode('utf-8')]:
			name += i
	else:
		name = 'NULL'
	if p.has_key("性别".decode('utf-8')):
		pline = [{}, {case_id: '1_0'}]
		pline[0]['type'.decode('utf-8')] = 'p'
		pline[0]['name'.decode('utf-8')] = name
		sex = p["性别".decode('utf-8')]
		if sex != []:
			if gender_map.has_key(sex[0]):
				sex_id = gender_map[sex[0]]
				gender_dict[sex_id]['4_' + str(p['id'])] = '8_0'
			else:
				sex_id = '9_' + str(attr_id)
				attr_id += 1
				gender_map[sex[0]] = sex_id
				gender_dict[sex_id] = {'4_' + str(p['id']): '8_0'}
			pline[1][sex_id] = '8_0'
		pr = p["户籍".decode('utf-8')]
		if p["户籍".decode('utf-8')] != []:
			if loco_map.has_key(pr[0]):
				pr_id = loco_map[pr[0]]
				loco_dict[pr_id]['4_' + str(p['id'])] = '6_2'
			else:
				pr_id = '1_' + str(loco_id)
				loco_id += 1
				loco_map[pr[0]] = pr_id
				loco_dict[pr_id] = {'4_' + str(p['id']): '6_2'}
			pline[1][pr_id] = '6_2'
			#pline[2]['register'.decode('utf-8')] = pr
		bir = p["出生年份".decode('utf-8')]
		if bir != []:
			if time_map.has_key(bir[0]):
				bir_id = time_map[bir[0]]
				time_dict[bir_id]['4_' + str(p['id'])] = '7_0'
			else:
				bir_id = '2_' + str(time_id)
				time_id += 1
				time_map[bir[0]] = bir_id
				time_dict[bir_id] = {'4_' + str(p['id']): '7_0'}
			pline[1][bir_id] = '7_0'
			#pline[2]['birthday'.decode('utf-8')] = bir[0]
		birp = p["出生地".decode('utf-8')]
		if birp != []:
			if loco_map.has_key(birp[0]):
				birp_id = loco_map[birp[0]]
				loco_dict[birp_id]['4_' + str(p['id'])] = '6_1'
			else:
				birp_id = '1_' + str(loco_id)
				loco_id += 1
				loco_map[birp[0]] = birp_id
				loco_dict[birp_id] = {'4_' + str(p['id']): '6_1'}
			pline[1][birp_id] = '6_1'
			#pline[2]['birthplace'.decode('utf-8')] = birp
		ethic = p["民族".decode('utf-8')]
		if ethic != []:
			if ethic_map.has_key(ethic[0]):
				ethic_id = ethic_map[ethic[0]]
				ethic_dict[ethic_id]['4_' + str(p['id'])] = '8_1'
			else:
				ethic_id = '9_' + str(attr_id)
				attr_id += 1
				ethic_map[ethic[0]] = ethic_id
				ethic_dict[ethic_id] = {'4_' + str(p['id']): '8_1'}
			pline[1][ethic_id] = '8_1'
			#pline[2]['ethic'.decode('utf-8')] = p['民族'.decode('utf-8')][0]
	elif len(name) < 6:
		pline = [{}, {case_id: '1_0'}]
		pline[0]['type'.decode('utf-8')] = 'p'
		pline[0]['name'.decode('utf-8')] = name
	else:
		pline = [{}, {case_id: '1_0'}]
		pline[0]['type'.decode('utf-8')] = 'i'
		#如果名称中的关键词在已有词典中都存在，则采用已有的id
		if p["姓名".decode('utf-8')] != []:
			pline[0]['name'.decode('utf-8')] = p["姓名".decode('utf-8')]
		reg = p["住所地".decode('utf-8')]
		if reg != []:
			if loco_map.has_key(reg[0]):
				reg_id = loco_map[reg[0]]
				loco_dict[reg_id]['3_' + str(p['id'])] = '6_0'
			else:
				reg_id = '1_' + str(loco_id)
				loco_id += 1
				loco_map[reg[0]] = reg_id
				loco_dict[reg_id] = {'3_' + str(p['id']): '6_0'}
			pline[1][reg_id] = '6_0'
		social = p["社会代码".decode('utf-8')]
		if social != '' and social != []:
			if social_map.has_key(social):
				social_id = social_map[social]
				social_dict[social_id]['3_' + str(p['id'])] = '8_2'
			else:
				social_id = '9_' + str(attr_id)
				attr_id += 1
				social_map[social] = social_id
				social_dict[social_id] = {'3_' + str(p['id']): '8_2'}
			pline[1][social_id] = '8_2'

	return pline, loco_id, time_id, lawfirm_id, attr_id

def lawyer_to_line(p, case_id, loco_id, time_id, lawfirm_id, attr_id):
	if p["姓名".decode('utf-8')] != []:
		name = ''
		for i in p["姓名".decode('utf-8')]:
			name += i
	else:
		name = 'NULL'
	pline = [{}, {case_id: '1_2'}]
	pid = '5_' + str(p['id'])
	pline[0]['name'] = name
	lawfirm = p["事务所及职位".decode('utf-8')]
	if lawfirm != []:
		firm = ''
		for i in lawfirm:
			if i != '事务所':
				firm += i
			else:
				firm += i
				break
		if lawfirm_map.has_key(firm):
			firm_id = lawfirm_map[firm]
			lawfirm_dict[firm_id][pid] = '8_3'
		else:
			firm_id = '6_' + str(lawfirm_id)
			lawfirm_id += 1
			lawfirm_map[firm] = firm_id
			lawfirm_dict[firm_id] = {pid: '8_3'}
		pline[1][firm_id] = '8_3'
	reg = p["地区".decode('utf-8')]
	if reg != []:
		if loco_map.has_key(reg[0]):
			reg_id = loco_map[reg[0]]
			loco_dict[reg_id][pid] = '6_0'
		else:
			reg_id = '1_' + str(loco_id)
			loco_id += 1
			loco_map[reg[0]] = reg_id
			loco_dict[reg_id] = {pid: '6_0'}
		pline[1][reg_id] = '6_0'
	lawyernum = p["执业证号".decode('utf-8')]
	if lawyernum != '' and lawyernum != []:
		if lawyernum_map.has_key(lawyernum[0]):
			lawyernum_id = lawyernum_map[lawyernum[0]]
			lawyernum_dict[lawyernum_id][pid] = '8_4'
		else:
			lawyernum_id = '9_' + str(attr_id)
			attr_id += 1
			lawyernum_map[lawyernum[0]] = lawyernum_id
			lawyernum_dict[lawyernum_id] = {pid: '8_4'}
		pline[1][lawyernum_id] = '8_4'

	return pline, loco_id, time_id, lawfirm_id, attr_id

def repre_to_line(p, case_id, loco_id, time_id, lawfirm_id, attr_id):
	pline = [{}, {case_id: '1_3'}]
	pline[0]['type'] = 'p'
	if p["姓名".decode('utf-8')] != []:
		name = ''
		for i in p["姓名".decode('utf-8')]:
			name += i
	else:
		name = 'NULL'
	pline[0]['name'] = name
	if p["职务".decode('utf-8')] != []:
		job = ''
		for i in p["职务".decode('utf-8')]:
			job += i
		pline[0]['job'] = job

	return pline, loco_id, time_id, lawfirm_id, attr_id

def tru_to_line(p, case_id, loco_id, time_id, lawfirm_id, attr_id):
	pline = [{}, {case_id: '1_4'}]
	pline[0]['type'] = 'p'
	pid = '4_' + str(p['id'])
	if p.has_key("职务".decode('utf-8')):
		if p["姓名".decode('utf-8')] != []:
			name = ''
			for i in p["姓名".decode('utf-8')]:
				name += i
		else:
			name = 'NULL'
		pline[0]['name'] = name
		if p["职务".decode('utf-8')] != []:
			job = ''
			for i in p["职务".decode('utf-8')]:
				job += i
			pline[0]['job'] = job
	else:
		if p["姓名".decode('utf-8')] != []:
			name = ''
			for i in p["姓名".decode('utf-8')]:
				name += i
		else:
			name = 'NULL'
		pline[0]['name'] = name
		sex = p["性别".decode('utf-8')]
		if sex != []:
			if gender_map.has_key(sex[0]):
				sex_id = gender_map[sex[0]]
				gender_dict[sex_id][pid] = '8_0'
			else:
				sex_id = '9_' + str(attr_id)
				attr_id += 1
				gender_map[sex[0]] = sex_id
				gender_dict[sex_id] = {pid: '8_0'}
			pline[1][sex_id] = '8_0'
		pr = p["户籍".decode('utf-8')]
		if p["户籍".decode('utf-8')] != []:
			if loco_map.has_key(pr[0]):
				pr_id = loco_map[pr[0]]
				loco_dict[pr_id][pid] = '6_2'
			else:
				pr_id = '1_' + str(loco_id)
				loco_id += 1
				loco_map[pr[0]] = pr_id
				loco_dict[pr_id] = {pid: '6_2'}
			pline[1][pr_id] = '6_2'
		bir = p["出生年份".decode('utf-8')]
		if bir != []:
			if time_map.has_key(bir[0]):
				bir_id = time_map[bir[0]]
				time_dict[bir_id][pid] = '7_0'
			else:
				bir_id = '2_' + str(time_id)
				time_id += 1
				time_map[bir[0]] = bir_id
				time_dict[bir_id] = {pid: '7_0'}
			pline[1][bir_id] = '7_0'
		birp = p["出生地".decode('utf-8')]
		if birp != []:
			if loco_map.has_key(birp[0]):
				birp_id = loco_map[birp[0]]
				loco_dict[birp_id][pid] = '6_1'
			else:
				birp_id = '1_' + str(loco_id)
				loco_id += 1
				loco_map[birp[0]] = birp_id
				loco_dict[birp_id] = {pid: '6_1'}
			pline[1][birp_id] = '6_1'
		ethic = p["民族".decode('utf-8')]
		if ethic != []:
			if ethic_map.has_key(ethic[0]):
				ethic_id = ethic_map[ethic[0]]
				ethic_dict[ethic_id][pid] = '8_1'
			else:
				ethic_id = '9_' + str(attr_id)
				attr_id += 1
				ethic_map[ethic[0]] = ethic_id
				ethic_dict[ethic_id] = {pid: '8_1'}
			pline[1][ethic_id] = '8_1'

	return pline, loco_id, time_id, lawfirm_id, attr_id

#案件（0），地区（1），时间（2），机构（3），当事人（4），律师（5），律所（6），法务（7），法院（8），属性（9）

def build_graph_from_json(json, case_id, loco_id, time_id, lawfirm_id, court_id, attr_id):

	court = json['法院'.decode('utf-8')]
	case = json['文书编号'.decode('utf-8')]
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
	case_line = {}

	cur_case_id = '0_' + str(case_id)
	case_map[cur_case_id] = case
	case_increment = True

	if not case_dict.has_key(cur_case_id):
		case_dict[cur_case_id] = case_line

	# 法院关系   5      0 审判长 1 审判员
	#第二步：检索法院，如果已存在，则直接赋已有的id，否则向字典中加入新的法院
	cur_court_id = ''
	court_line = {}
	if court != '':
		if court_map.has_key(court):
			cur_court_id = court_map[court]
			court_line = court_dict[cur_court_id]
			court_line[cur_case_id] = '1_7'
		else:
			cur_court_id = '8_' + str(court_id)
			court_map[court] = '8_' + str(court_id)
			court_line = {cur_case_id: '1_7'}
			court_increment = True
		case_dict[cur_case_id][cur_court_id] = '1_7'

	if not court_dict.has_key(cur_court_id):
		court_dict[cur_court_id] = court_line

	# 法院关系   5      0 审判长 1 审判员
	#第三步：建立法务人员与法院的关系
	for item in law_worker:
		posi = item['职务'.decode('utf-8')][0]
		na = item['姓名'.decode('utf-8')][0]
		lid = '7_' + str(item['id'])
		if posi == '审判长':
			if cur_court_id != '':
				lawworker_dict[lid] = {cur_court_id: '5_0', cur_case_id: '1_5'}
			#p_f.write(js.dumps([[cur_case_id], str(item['id']), {'name': na}, {cur_court_id: '5_0', cur_case_id: '1_5'}], ensure_ascii=False) + '\n')
			else:
				lawworker_dict[lid] = {cur_case_id: '1_5'}
				#p_f.write(js.dumps([[cur_case_id], str(item['id']), {'name': na}, {cur_case_id: '1_5'}],ensure_ascii=False) + '\n')
			case_dict[cur_case_id][lid] = '1_5'
			court_dict[cur_court_id][lid] = '5_0'
			lawworker_map[lid] = {'name': na}
		elif posi == '审判员':
			if cur_court_id != '':
				lawworker_dict[lid] = {cur_court_id: '5_1', cur_case_id: '1_6'}
				#p_f.write(js.dumps([[cur_case_id], str(item['id']), {'name': na}, {cur_court_id: '5_1', cur_case_id: '1_6'}],ensure_ascii=False) + '\n')
			else:
				lawworker_dict[lid] = {cur_case_id: '1_6'}
				#p_f.write(js.dumps([[cur_case_id], str(item['id']), {'name': na}, {cur_case_id: '1_6'}],ensure_ascii=False) + '\n')
			case_dict[cur_case_id][lid] = '1_6'
			court_dict[cur_court_id][lid] = '5_1'
			lawworker_map[lid] = {'name': na}

	#第三步：建立当事人、当事机构和律师之间的关系
	tmp_person_dict = {}
	tmp_inst_dict = {}
	tmp_lawyer_dict = {}

	for p in prosecu:
		pline, loco_id, time_id, lawfirm_id, attr_id = dict_to_line(p, cur_case_id, loco_id, time_id, lawfirm_id, attr_id)
		pid = str(p['id'])
		for d in defend:
			if d.has_key("性别".decode('utf-8')):
				pline[1]['4_' + str(d['id'])] = '2_1'
			else:
				pline[1]['3_' + str(d['id'])] = '2_1'
		if pline[0]['type'] == 'p':
			pid = '4_' + pid
			pline[0].pop('type')
			tmp_person_dict[pid] = pline[1]
			person_map[pid] = pline[0]
		else:
			pid = '3_' + pid
			pline[0].pop('type')
			tmp_inst_dict[pid] = pline[1]
			inst_map[pid] = pline[0]
		case_dict[cur_case_id][pid] = '1_0'

	for d in defend:
		dline, loco_id, time_id, lawfirm_id, attr_id = dict_to_line(d, cur_case_id, loco_id, time_id, lawfirm_id, attr_id)
		did = str(d['id'])
		for p in prosecu:
			if p.has_key("性别".decode('utf-8')):
				dline[1]['4_' + str(p['id'])] = '2_0'
			else:
				dline[1]['3_' + str(p['id'])] = '2_0'
		if dline[0]['type'] == 'p':
			did = '4_' + did
			dline[0].pop('type')
			tmp_person_dict[did] = dline[1]
			person_map[did] = dline[0]
		else:
			did = '3_' + did
			dline[0].pop('type')
			tmp_inst_dict[did] = dline[1]
			inst_map[did] = dline[0]
		case_dict[cur_case_id][did] = '1_1'

	for a in advocate:
		aline, loco_id, time_id, lawfirm_id, attr_id = lawyer_to_line(a, cur_case_id, loco_id, time_id, lawfirm_id, attr_id)
		id = str(a['代理方id'.decode('utf-8')])
		aid = '5_' + str(a['id'])
		if tmp_person_dict.has_key('4_' + id):
			tmp_person_dict['4_' + id][aid] = '3_0'
			aline[1]['4_' + id] = '3_1'
			tmp_lawyer_dict[aid] = aline[1]
			lawyer_map[aid] = aline[0]
		elif tmp_inst_dict.has_key('3_' + id):
			tmp_inst_dict['3_' + id][aid] = '3_0'
			aline[1]['3_' + id] = '3_1'
			tmp_lawyer_dict[aid] = aline[1]
			lawyer_map[aid] = aline[0]
		case_dict[cur_case_id][aid] = '1_2'

	for l in lawyer:
		lline, loco_id, time_id, lawfirm_id, attr_id = lawyer_to_line(l, cur_case_id, loco_id, time_id, lawfirm_id, attr_id)
		id = str(l['代理方id'.decode('utf-8')])
		lid = '5_' + str(l['id'])
		if tmp_person_dict.has_key('4_' + id):
			tmp_person_dict['4_' + id][lid] = '4_2'
			lline[1]['4_' + id] = '4_3'
			tmp_lawyer_dict[lid] = lline[1]
			lawyer_map[lid] = lline[0]
		elif tmp_inst_dict.has_key('3_' + id):
			tmp_inst_dict['3_' + id][lid] = '4_2'
			lline[1]['3_' + id] = '4_3'
			tmp_lawyer_dict[lid] = lline[1]
			lawyer_map[lid] = lline[0]
		case_dict[cur_case_id][lid] = '1_3'

	for r in represen:
		rline, loco_id, time_id, lawfirm_id, attr_id = repre_to_line(r, cur_case_id, loco_id, time_id, lawfirm_id, attr_id)
		id = str(r['代理方id'.decode('utf-8')])
		rid = '4_' + str(r['id'])
		if tmp_person_dict.has_key('4_' + id):
			tmp_person_dict['4_' + id][rid] = '4_0'
			rline[1]['4_' + id] = '4_1'
			tmp_person_dict[rid] = rline[1]
			person_map[rid] = rline[0]
		elif tmp_inst_dict.has_key('3_' + id):
			tmp_inst_dict['3_' + id][rid] = '4_0'
			rline[1]['3_' + id] = '4_1'
			tmp_person_dict[rid] = rline[1]
			person_map[rid] = rline[0]
		case_dict[cur_case_id][rid] = '1_3'

	for t in trustee:
		tline, loco_id, time_id, lawfirm_id, attr_id = tru_to_line(t, cur_case_id, loco_id, time_id, lawfirm_id, attr_id)
		id = str(t['代理方id'.decode('utf-8')])
		tid = '4_' + str(t['id'])
		if tmp_person_dict.has_key('4_' + id):
			tmp_person_dict['4_' + id][tid] = '4_2'
			tline[1]['4_' + id] = '4_3'
			tmp_person_dict[tid] = tline[1]
			person_map[tid] = tline[0]
		elif tmp_inst_dict.has_key('3_' + id):
			tmp_inst_dict['3_' + id][tid] = '4_2'
			tline[1]['3_' + id] = '4_3'
			tmp_person_dict[tid] = tline[1]
			person_map[tid] = tline[0]
		case_dict[cur_case_id][tid] = '1_4'

	#第四步 建立当前所有人与案件本身的关系


	#第五步：打印输出
	#f.write(js.dumps(case_line, ensure_ascii=False) + '\n')

	person_dict.update(tmp_person_dict)
	inst_dict.update(tmp_inst_dict)
	'''
	for i in tmp_person_dict.items():
		key = i[0]
		value = i[1]
		if value[0]['type'] == 'p':
			if value[0].has_key('type'):
				value[0].pop('type')
			if value[0].has_key('prosecu'):
				value[0].pop('prosecu')
			person_dict[key] = value
			#p_f.write(js.dumps(i, ensure_ascii=False) + '\n')
		else:
			if value[0].has_key('type'):
				value[0].pop('type')
			if value[0].has_key('prosecu'):
				value[0].pop('prosecu')
			inst_dict[key] = value
			#i_f.write(js.dumps(i, ensure_ascii=False) + '\n')
	'''
	#for i in advocate_dict.values():
		#p_f.write(js.dumps(i, ensure_ascii=False) + '\n')
	lawyer_dict.update(tmp_lawyer_dict)
	#for i in tmp_lawyer_dict.items():
		#p_f.write(js.dumps(i, ensure_ascii=False) + '\n')

	if case_increment:
		case_id += 1
	if court_increment:
		court_id += 1

	return case_id, loco_id, time_id, lawfirm_id, court_id, attr_id


f = open('content_json_sample.txt', 'r')

case_graph = open('case_graph.txt', 'w')
f_case_map = open('case_map.txt', 'w')
loco_graph = open('loco_graph.txt', 'w')
f_loco_map = open('loco_map.txt', 'w')
time_graph = open('time_graph.txt', 'w')
f_time_map = open('time_map.txt', 'w')
person_graph = open('person_graph.txt', 'w')
f_person_map = open('person_map.txt', 'w')
inst_graph = open('inst_graph.txt', 'w')
f_inst_map = open('inst_map.txt', 'w')
gender_graph = open('gender_graph.txt', 'w')
f_gender_map = open('gender_map.txt', 'w')
ethic_graph = open('ethic_graph.txt', 'w')
f_ethic_map = open('ethic_map.txt', 'w')
social_graph = open('social_graph.txt', 'w')
f_social_map = open('social_map.txt', 'w')
lawyer_graph = open('lawyer_graph.txt', 'w')
f_lawyer_map = open('lawyer_map.txt', 'w')
lawfirm_graph = open('lawfirm_graph.txt', 'w')
f_lawfirm_map = open('lawfirm_map.txt', 'w')
lawyernum_graph = open('lawyernum_graph.txt', 'w')
f_lawyernum_map = open('lawyernum_map.txt', 'w')
lawworker_graph = open('lawworker_graph.txt', 'w')
f_lawworker_map = open('lawworker_map.txt', 'w')
court_graph = open('court_graph.txt', 'w')
f_court_map = open('court_map.txt', 'w')

case_id = 0
loco_id = 0
time_id = 0
lawfirm_id = 0
court_id = 0
attr_id = 0

for l in f:
	if l != '\n':
		json = js.loads(l)
		case_id, loco_id, time_id, lawfirm_id, court_id, attr_id = build_graph_from_json(json, case_id, loco_id, time_id, lawfirm_id, court_id, attr_id)

case_graph.write("Total vertices: " + str(len(case_dict)))
for i in case_dict.items():
	case_graph.write(i[0] + '&')
	tmp = ''
	for j in i[1].items():
		tmp += j[0] + ':' + j[1] + ' '
	case_graph.write(tmp.rstrip() + '\n')

f_case_map.write("Total vertices: " + str(len(case_map)) + '\n')
for i in case_map.items():
	features = i[1]
	# print type(features)
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
	f_case_map.write(i[0] + '&' + name + '\n')

loco_graph.write("Total vertices: " + str(len(loco_dict)) + '\n')
for i in loco_dict.items():
	loco_graph.write(i[0] + '&')
	tmp = ''
	for j in i[1].items():
		tmp += j[0] + ':' + j[1] + ' '
	loco_graph.write(tmp.rstrip() + '\n')

f_loco_map.write("Total vertices: " + str(len(loco_map)) + '\n')
for i in loco_map.items():
	features = i[0]
	# print type(features)
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
	f_loco_map.write(i[1] + '&' + name + '\n')

time_graph.write("Total vertices: " + str(len(time_dict)) + '\n')
for i in time_dict.items():
	time_graph.write(i[0] + '&')
	tmp = ''
	for j in i[1].items():
		tmp += j[0] + ':' + j[1] + ' '
	time_graph.write(tmp.rstrip() + '\n')

f_time_map.write("Total vertices: " + str(len(time_map)) + '\n')
for i in time_map.items():
	features = i[0]
	# print type(features)
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
	f_time_map.write(i[1] + '&' + name + '\n')

person_graph.write("Total vertices: " + str(len(person_dict)) + '\n')
for i in person_dict.items():
	person_graph.write(i[0] + '&')
	tmp = ''
	for j in i[1].items():
		tmp += j[0] + ':' + j[1] + ' '
	person_graph.write(tmp.rstrip() + '\n')

f_person_map.write("Total vertices: " + str(len(person_map)) + '\n')
for i in person_map.items():
	features = i[1]
	# print type(features)
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
	f_person_map.write(i[0] + '&' + name + '\n')

inst_graph.write("Total vertices: " + str(len(inst_dict)) + '\n')
for i in inst_dict.items():
	inst_graph.write(i[0] + '&')
	tmp = ''
	for j in i[1].items():
		tmp += j[0] + ':' + j[1] + ' '
	inst_graph.write(tmp.rstrip() + '\n')

f_inst_map.write("Total vertices: " + str(len(inst_map)) + '\n')
for i in inst_map.items():
	features = i[1]
	# print type(features)
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
	f_inst_map.write(i[0] + '&' + name + '\n')

gender_graph.write("Total vertices: " + str(len(gender_dict)) + '\n')
for i in gender_dict.items():
	gender_graph.write(i[0] + '&')
	tmp = ''
	for j in i[1].items():
		tmp += j[0] + ':' + j[1] + ' '
	gender_graph.write(tmp.rstrip() + '\n')

f_gender_map.write("Total vertices: " + str(len(gender_map)) + '\n')
for i in gender_map.items():
	features = i[0]
	# print type(features)
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
	f_gender_map.write(i[1] + '&' + name + '\n')

ethic_graph.write("Total vertices: " + str(len(ethic_dict)) + '\n')
for i in ethic_dict.items():
	ethic_graph.write(i[0] + '&')
	tmp = ''
	for j in i[1].items():
		tmp += j[0] + ':' + j[1] + ' '
	ethic_graph.write(tmp.rstrip() + '\n')

f_ethic_map.write("Total vertices: " + str(len(ethic_map)) + '\n')
for i in ethic_map.items():
	features = i[0]
	# print type(features)
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
	f_ethic_map.write(i[1] + '&' + name + '\n')

social_graph.write("Total vertices: " + str(len(social_dict)) + '\n')
for i in social_dict.items():
	social_graph.write(i[0] + '&')
	tmp = ''
	for j in i[1].items():
		tmp += j[0] + ':' + j[1] + ' '
	social_graph.write(tmp.rstrip() + '\n')

f_social_map.write("Total vertices: " + str(len(social_map)) + '\n')
for i in social_map.items():
	features = i[0]
	# print type(features)
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
	f_social_map.write(i[1] + '&' + name + '\n')

lawyer_graph.write("Total vertices: " + str(len(lawyer_dict)) + '\n')
for i in lawyer_dict.items():
	lawyer_graph.write(i[0] + '&')
	tmp = ''
	for j in i[1].items():
		tmp += j[0] + ':' + j[1] + ' '
	lawyer_graph.write(tmp.rstrip() + '\n')

f_lawyer_map.write("Total vertices: " + str(len(lawyer_map)) + '\n')
for i in lawyer_map.items():
	features = i[1]
	# print type(features)
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
	f_lawyer_map.write(i[0] + '&' + name + '\n')

lawfirm_graph.write("Total vertices: " + str(len(lawfirm_dict)) + '\n')
for i in lawfirm_dict.items():
	lawfirm_graph.write(i[0] + '&')
	tmp = ''
	for j in i[1].items():
		tmp += j[0] + ':' + j[1] + ' '
	lawfirm_graph.write(tmp.rstrip() + '\n')

f_lawfirm_map.write("Total vertices: " + str(len(lawfirm_map)) + '\n')
for i in lawfirm_map.items():
	features = i[0]
	# print type(features)
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
	f_lawfirm_map.write(i[1] + '&' + name + '\n')

lawyernum_graph.write("Total vertices: " + str(len(lawyernum_dict)) + '\n')
for i in lawyernum_dict.items():
	lawyernum_graph.write(i[0] + '&')
	tmp = ''
	for j in i[1].items():
		tmp += j[0] + ':' + j[1] + ' '
	lawyernum_graph.write(tmp.rstrip() + '\n')

f_lawyernum_map.write("Total vertices: " + str(len(lawyernum_map)) + '\n')
for i in lawyernum_map.items():
	features = i[0]
	# print type(features)
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
	f_lawyernum_map.write(i[1] + '&' + name + '\n')

lawworker_graph.write("Total vertices: " + str(len(lawworker_dict)) + '\n')
for i in lawworker_dict.items():
	lawworker_graph.write(i[0] + '&')
	tmp = ''
	for j in i[1].items():
		tmp += j[0] + ':' + j[1] + ' '
	lawworker_graph.write(tmp.rstrip() + '\n')

f_lawworker_map.write("Total vertices: " + str(len(lawworker_map)) + '\n')
for i in lawworker_map.items():
	features = i[1]
	# print type(features)
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
	f_lawworker_map.write(i[0] + '&' + name + '\n')

court_graph.write("Total vertices: " + str(len(court_dict)) + '\n')
for i in court_dict.items():
	court_graph.write(i[0] + '&')
	tmp = ''
	for j in i[1].items():
		tmp += j[0] + ':' + j[1] + ' '
	court_graph.write(tmp.rstrip() + '\n')

f_court_map.write("Total vertices: " + str(len(court_map)) + '\n')
for i in court_map.items():
	features = i[0]
	# print type(features)
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
	f_court_map.write(i[1] + '&' + name + '\n')

#case_graph.write(js.dumps(case_dict, ensure_ascii=False) + '\n')
#f_case_map.write(js.dumps(case_map, ensure_ascii=False) + '\n')
#loco_graph.write(js.dumps(loco_dict, ensure_ascii=False) + '\n')
#f_loco_map.write(js.dumps(dict(zip(loco_map.values(), loco_map.keys())), ensure_ascii=False) + '\n')
#time_graph.write(js.dumps(time_dict, ensure_ascii=False) + '\n')
#f_time_map.write(js.dumps(dict(zip(time_map.values(), time_map.keys())), ensure_ascii=False) + '\n')
#person_graph.write(js.dumps(person_dict, ensure_ascii=False) + '\n')
#f_person_map.write(js.dumps(person_map, ensure_ascii=False) + '\n')
#inst_graph.write(js.dumps(inst_dict, ensure_ascii=False) + '\n')
#f_inst_map.write(js.dumps(inst_map, ensure_ascii=False) + '\n')
#gender_graph.write(js.dumps(gender_dict, ensure_ascii=False) + '\n')
#f_gender_map.write(js.dumps(dict(zip(gender_map.values(), gender_map.keys())), ensure_ascii=False) + '\n')
#ethic_graph.write(js.dumps(ethic_dict, ensure_ascii=False) + '\n')
#f_ethic_map.write(js.dumps(dict(zip(ethic_map.values(), ethic_map.keys())), ensure_ascii=False) + '\n')
#social_graph.write(js.dumps(social_dict, ensure_ascii=False) + '\n')
#f_social_map.write(js.dumps(dict(zip(social_map.values(), social_map.keys())), ensure_ascii=False) + '\n')
#lawyer_graph.write(js.dumps(lawyer_dict, ensure_ascii=False) + '\n')
#f_lawyer_map.write(js.dumps(lawyer_map, ensure_ascii=False) + '\n')
#lawfirm_graph.write(js.dumps(lawfirm_dict, ensure_ascii=False) + '\n')
#f_lawfirm_map.write(js.dumps(dict(zip(lawfirm_map.values(), lawfirm_map.keys())), ensure_ascii=False) + '\n')
#lawyernum_graph.write(js.dumps(lawyernum_dict, ensure_ascii=False) + '\n')
#f_lawyernum_map.write(js.dumps(dict(zip(lawyernum_map.values(), lawyernum_map.keys())), ensure_ascii=False) + '\n')
#lawworker_graph.write(js.dumps(lawworker_dict, ensure_ascii=False) + '\n')
#f_lawworker_map.write(js.dumps(lawworker_map, ensure_ascii=False) + '\n')
#court_graph.write(js.dumps(court_dict, ensure_ascii=False) + '\n')
#f_court_map.write(js.dumps(dict(zip(court_map.values(), court_map.keys())), ensure_ascii=False) + '\n')