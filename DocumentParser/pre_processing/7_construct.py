#coding=utf-8
from __future__ import division
import os
import sys
import json

class Constructor:
    def __init__(self):
        '''serial_id标识当下实体的唯一id，每次创建新的Constructor都应当传入当前id；corporate_table提供可查询的职务名称表'''
        self.serial_id = 0
        self.corporate_table = ['董事长', '经理', '厂长']
        self.former_entity_id = -1
        return

    def _flag_extract(self, label, key, start_flag, end_flag, obj, keys, in_process, sect_count):
        '''
        if sect_count > len(label) - 1:
            dict[dict_key].append(obj)
            return [in_process, skip, sect_count]
        '''

        if start_flag[sect_count] == 'NONE':
            in_process = True

        if not in_process and start_flag[sect_count] == keys[0]:
            in_process = True
        elif end_flag[sect_count] == keys[1] or end_flag[sect_count] == keys[0]:
            in_process = False
            sect_count += 1
        elif in_process and (keys[1] == label[sect_count] or label[sect_count] == 'NONE'):
            obj[key[sect_count]].append(keys[0])

        if in_process and sect_count < len(label) and end_flag[sect_count] == 'NONE':
            sect_count += 1
            in_process = False

        return [in_process, sect_count]

    def construct(self, file_list, serial_id):
        self.serial_id = serial_id
        '''mode: 0 公诉机关 1 原告 2 被告 3 律师 4 审判员、陪审员、书记员'''
        dict = {'法院': '', '公诉机关': '', '文书类型': '', '文书编号': '', '原告': [], '被告':[], '辩护人': [], '代理律师': [], '法务人员': [], '法定代表人': [],'委托代理人': []}
        person_label = ['np', 'a', 't', 'ns', 'nz', 'ns']
        person_key = ['姓名', '性别', '出生年份', '出生地', '民族', '户籍']
        person_start_flag = ['NONE', 'NONE', 'NONE', '于', 'NONE', '户籍']
        person_end_flag = ['，', '，', 'NONE', 'w', 'w', '。']
        defender_label = ['np', 'ns', 'NONE', 'm']
        defender_key = ['姓名', '地区', '事务所及职位', '执业证号']
        defender_start_flag = ['NONE', 'NONE', 'NONE', 'NONE']
        defender_end_flag = ['，', 'NONE', '。', '。']


        for line in file_list:
            line = line.strip()
            mode = -1
            sub_mode = -1
            words = line.split(' ')
            sect_count = 0
            word_count = 0
            in_process = False
            person = {'id': -1, '姓名': [], '性别': [], '出生年份': [], '出生地': [], '民族': [], '户籍': [], '代理方id': -1}
            defender = {'id': -1, '姓名': [], '地区': [], '事务所及职位': [], '执业证号': [], '代理方id': -1}
            lawman = {'id': -1, '姓名': [], '职务': []}
            institute = {'id': -1, '姓名': [], '住所地': [], '社会代码': []}
            corporate = {'id': -1, '姓名': [], '职务': [], '代理方id': -1}
            skip = False
            prev = ''
            for word in words:
                word_count += 1
                if mode == -1:
                    if word == '上诉人_n' or word == '原告人_n' or word == '原告_n' or word == '申请人_n':
                        self.former_entity_id = self.serial_id
                        person['id'] = self.serial_id
                        institute['id'] = self.serial_id
                        mode = 1
                    elif word == '被告人_n' or word == '被告_n' or word == '被上诉人_n' or word == '罪犯_n':
                        self.former_entity_id = self.serial_id
                        person['id'] = self.serial_id
                        institute['id'] = self.serial_id
                        mode = 2
                    elif word == '辩护人_n':
                        defender['id'] = self.serial_id
                        defender['代理方id'] = self.former_entity_id
                        mode = 3
                    elif word == '审判长_n' or word == '审判员_n' or word == '书记员_n' or word == '陪审员_n':
                        self.former_entity_id = self.serial_id
                        lawman['id'] = self.serial_id
                        lawman['职务'].append(word.split('_')[0])
                        mode = 4
                    elif word == '代表人_n' or word == '负责人_n':
                        mode = 7
                        corporate['代理方id'] = self.former_entity_id
                        corporate['id'] = self.serial_id
                        for corp in self.corporate_table:
                            if corp in line:
                                corporate['职务'].append(corp)
                    elif word == '代理人_n':
                        if '律师_n' in line or '法律_n' in line:
                            defender['id'] = self.serial_id
                            defender['代理方id'] = self.former_entity_id
                            mode = 8
                        else:
                            person['id'] = self.serial_id
                            person['代理方id'] = self.former_entity_id
                            mode = 10
                            for corp in self.corporate_table:
                                if corp in line:
                                    corporate['代理方id'] = self.former_entity_id
                                    corporate['id'] = self.serial_id
                                    corporate['职务'].append(corp)
                                    mode = 9
                    elif word == '第三人':
                        pass
                    elif word == '被_p' or word == '申请_v':
                        prev = word
                    elif word == '执行人_n':
                        if prev == '申请_v':
                            self.former_entity_id = self.serial_id
                            person['id'] = self.serial_id
                            institute['id'] = self.serial_id
                            mode = 1
                            prev = ''
                        elif prev == '被_p':
                            self.former_entity_id = self.serial_id
                            person['id'] = self.serial_id
                            institute['id'] = self.serial_id
                            mode = 2
                            prev = ''
                    else:
                        mode = -1
                else:
                    try:
                        keys = word.split('_')
                        if mode == 0:
                            if word_count > len(words) - 1:
                                dict['法院'].append(court)
                                self.serial_id += 1
                            elif keys[1] == 'ns':
                                court['姓名'].append(keys[0])
                        elif mode == 1:
                            if sub_mode == 1:
                                feedback = self._flag_extract(person_label, person_key, person_start_flag,
                                                              person_end_flag,
                                                              person, keys, in_process, sect_count)
                                in_process = feedback[0]
                                sect_count = feedback[1]
                                if sect_count > len(person_label) - 1 or word_count > len(words) - 1:
                                    dict['原告'].append(person)
                                    self.serial_id += 1
                                    break
                            elif sub_mode == 2:
                                if word_count > len(words) - 1:
                                    dict['原告'].append(institute)
                                    self.serial_id += 1
                                    break
                                elif sect_count == 0:
                                    if keys[0] == '，' or keys[0] == '。' or keys[0] == ',' or keys[0] == '.':
                                        sect_count += 1
                                    else:
                                        institute['姓名'].append(keys[0])
                                elif sect_count == 1:
                                    if keys[0] == '代码':
                                        sect_count = 2
                                    elif keys[0] == '地':
                                        sect_count = 3
                                elif sect_count == 2:
                                    if keys[1] == 'm':
                                        institute['社会代码'] = keys[0]
                                        sect_count = 1
                                elif sect_count == 3:
                                    if keys[0] == '，' or keys[0] == '。':
                                        sect_count = 1
                                    else:
                                        institute['住所地'].append(keys[0])
                            else:
                                if skip:
                                    if keys[0] == '）':
                                        skip = False
                                elif keys[1] == 'np':
                                    feedback = self._flag_extract(person_label, person_key, person_start_flag,
                                                                  person_end_flag,
                                                                  person, keys, in_process, sect_count)
                                    in_process = feedback[0]
                                    sect_count = feedback[1]
                                    if sect_count > len(person_label) - 1 or word_count > len(words) - 1:
                                        dict['原告'].append(person)
                                        self.serial_id += 1
                                        break
                                    sub_mode = 1
                                elif keys[0] == '（':
                                    skip = True
                                else:
                                    if word_count > len(words) - 1:
                                        dict['原告'].append(institute)
                                        self.serial_id += 1
                                        break
                                    elif sect_count == 0:
                                        if keys[0] == '，' or keys[0] == '。' or keys[0] == ',' or keys[0] == '.':
                                            sect_count += 1
                                        else:
                                            institute['姓名'].append(keys[0])
                                    elif sect_count == 1:
                                        if keys[0] == '代码':
                                            sect_count = 2
                                        elif keys[0] == '地':
                                            sect_count = 3
                                    elif sect_count == 2:
                                        if keys[1] == 'm':
                                            institute['社会代码'] = keys[0]
                                            sect_count = 1
                                    elif sect_count == 3:
                                        if keys[0] == '，' or keys[0] == '。':
                                            sect_count = 1
                                        else:
                                            institute['住所地'].append(keys[0])
                                    sub_mode = 2
                        elif mode == 2:
                            if sub_mode == 1:
                                feedback = self._flag_extract(person_label, person_key, person_start_flag,
                                                              person_end_flag,
                                                              person, keys, in_process, sect_count)
                                in_process = feedback[0]
                                sect_count = feedback[1]
                                if sect_count > len(person_label) - 1 or word_count > len(words) - 1:
                                    dict['被告'].append(person)
                                    self.serial_id += 1
                                    break
                            elif sub_mode == 2:
                                if word_count > len(words) - 1:
                                    dict['被告'].append(institute)
                                    self.serial_id += 1
                                    break
                                elif sect_count == 0:
                                    if keys[0] == '，' or keys[0] == '。' or keys[0] == ',' or keys[0] == '.':
                                        sect_count += 1
                                    else:
                                        institute['姓名'].append(keys[0])
                                elif sect_count == 1:
                                    if keys[0] == '代码':
                                        sect_count = 2
                                    elif keys[0] == '地':
                                        sect_count = 3
                                elif sect_count == 2:
                                    if keys[1] == 'm':
                                        institute['社会代码'] = keys[0]
                                        sect_count = 1
                                elif sect_count == 3:
                                    if keys[0] == '，' or keys[0] == '。':
                                        sect_count = 1
                                    else:
                                        institute['住所地'].append(keys[0])
                            else:
                                if skip:
                                    if keys[0] == '）':
                                        skip = False
                                elif keys[1] == 'np':
                                    feedback = self._flag_extract(person_label, person_key, person_start_flag,
                                                                  person_end_flag,
                                                                  person, keys, in_process, sect_count)
                                    in_process = feedback[0]
                                    sect_count = feedback[1]
                                    if sect_count > len(person_label) - 1 or word_count > len(words) - 1:
                                        dict['被告'].append(person)
                                        self.serial_id += 1
                                        break
                                    sub_mode = 1
                                elif keys[0] == '（':
                                    skip = True
                                else:
                                    if word_count > len(words) - 1:
                                        dict['被告'].append(institute)
                                        self.serial_id += 1
                                        break
                                    elif sect_count == 0:
                                        if keys[0] == '，' or keys[0] == '。' or keys[0] == ',' or keys[0] == '.':
                                            sect_count += 1
                                        else:
                                            institute['姓名'].append(keys[0])
                                    elif sect_count == 1:
                                        if keys[0] == '代码':
                                            sect_count = 2
                                        elif keys[0] == '地':
                                            sect_count = 3
                                    elif sect_count == 2:
                                        if keys[1] == 'm':
                                            institute['社会代码'] = keys[0]
                                            sect_count = 1
                                    elif sect_count == 3:
                                        if keys[0] == '，' or keys[0] == '。':
                                            sect_count = 1
                                        else:
                                            institute['住所地'].append(keys[0])
                                    sub_mode = 2
                        elif mode == 3:
                            feedback = self._flag_extract(defender_label, defender_key, defender_start_flag,
                                                          defender_end_flag, defender, keys, in_process, sect_count)
                            in_process = feedback[0]
                            sect_count = feedback[1]
                            if sect_count > len(defender_label) - 1 or word_count > len(words) - 1:
                                dict['辩护人'].append(defender)
                                self.serial_id += 1
                                break
                        elif mode == 4:
                            lawman['姓名'].append(keys[0])
                            dict['法务人员'].append(lawman)
                            self.serial_id += 1
                            break
                        elif mode == 7:
                            if keys[1] == 'np':
                                corporate['姓名'].append(keys[0])
                                dict['法定代表人'].append(corporate)
                                self.serial_id += 1
                                break
                        elif mode == 8:
                            feedback = self._flag_extract(defender_label, defender_key, defender_start_flag,
                                                          defender_end_flag, defender, keys, in_process, sect_count)
                            in_process = feedback[0]
                            sect_count = feedback[1]
                            if sect_count > len(defender_label) - 1 or word_count > len(words) - 1:
                                dict['代理律师'].append(defender)
                                self.serial_id += 1
                                break
                        elif mode == 9:
                            if word_count > len(words) - 1:
                                dict['委托代理人'].append(corporate)
                                self.serial_id += 1
                                break
                            elif keys[1] == 'np':
                                corporate['姓名'].append(keys[1])
                        elif mode == 10:
                            feedback = self._flag_extract(person_label, person_key, person_start_flag, person_end_flag,
                                                          person, keys, in_process, sect_count)
                            in_process = feedback[0]
                            sect_count = feedback[1]
                            if sect_count > len(person_label) - 1 or word_count > len(words) - 1:
                                dict['委托代理人'].append(person)
                                self.serial_id += 1
                                break
                    except Exception, e:    
                        sys.stdout.write(str(e) + '\nInvalid Format!\n')
        return [self.serial_id, dict]

con = Constructor()
serial_id = 0
line_count = 0
file_count = 0
court = ''
doc_type = ''
case_id = ''
procu = ''
f = open(sys.argv[1] + '_merge', 'r')
o = open(sys.argv[1] + '_json', 'w')
file_list = []
start = False

for line in f:
    if line != '\n':

        if line == '标题结束\n':
            court = file_list[0]
            doc_type = file_list[1]
            case_id = file_list[2]
            if len(file_list) == 4:
                procu = file_list[3]
            start = True
            file_list = []
        else:
            file_list.append(line)
    elif start:
        struct = con.construct(file_list, serial_id)
        serial_id = struct[0]
        dict = struct[1]
        dict['法院'] = court
        dict['文书类型'] = doc_type
        dict['文书编号'] = case_id
        dict['公诉机关'] = procu
        o.write(json.dumps(dict, ensure_ascii=False))
        o.write('\n\n')
        court = ''
        doc_type = ''
        case_id = ''
        procu = ''
        start = False
        file_list = []
    else:
        court = ''
        doc_type = ''
        case_id = ''
        procu = ''
        start = False
        file_list = []

