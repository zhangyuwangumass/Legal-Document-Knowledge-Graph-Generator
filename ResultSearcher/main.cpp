#include <iostream>
#include <algorithm>
#include <fstream>
#include <vector>
#include <map>

/**
#相等关系   0      0~1，概率
#当事关系   1      0 原告 1 被告 2 律师 3 代表人 4 代理人 5 审判长 6 审判员 7 法院
#诉讼关系   2      0 被诉 1 起诉
#辩护关系   3      0 被辩护 1 辩护
#代表关系   4      0 被代表 1 代表 2 被委托（代理） 3 委托（被代理）
#法院关系   5      0 审判长 1 审判员
#地点关系   6      0 住所地 1 出生地 2 户籍地
#时间关系   7      0 出生日期 1 判决日期
#属性关系   8      0 性别 1 民族 2 机构社会编号 3 律所 4 律师执业证号
**/

static std::string edge_matrix[9][8] = {{"相等", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL","NULL"},
                                        {"当事人", "当事人", "律师", "代表人", "代理人", "审判长", "审判员", "法院"},
                                        {"被诉", "起诉", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL"},
                                        {"被辩护", "辩护", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL"},
                                        {"被代表", "代表", "委托（被代理）", "被委托（代理）", "NULL", "NULL", "NULL", "NULL"},
                                        {"审判长", "审判员", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL"},
                                        {"住所地", "出生地", "户籍地", "NULL", "NULL", "NULL", "NULL", "NULL"},
                                        {"出生日期", "判决日期", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL"},
                                        {"性别", "民族", "机构社会编号", "律所", "律师执业证号", "NULL", "NULL", "NULL"}};

//#args: case, loco, time, person, inst, gender, ethic, social, lawyer, lawfirm, lawyernum, lawworker, court
std::vector<int> files_len = {13, 13, 2};
const std::string path = "data/";
std::vector<std::string> graph_files = {"case_graph.txt", "loco_graph.txt",
                                       "time_graph.txt", "person_graph.txt",
                                       "inst_graph.txt", "gender_graph.txt",
                                       "ethic_graph.txt", "social_graph.txt",
                                       "lawyer_graph.txt", "lawfirm_graph.txt",
                                       "lawyernum_graph.txt", "lawworker_graph.txt",
                                       "court_graph.txt"};

std::vector<std::string> map_files = {"case_map.txt", "loco_map.txt",
                                       "time_map.txt", "person_map.txt",
                                       "inst_map.txt", "gender_map.txt",
                                       "ethic_map.txt", "social_map.txt",
                                       "lawyer_map.txt", "lawfirm_map.txt",
                                       "lawyernum_map.txt", "lawworker_map.txt",
                                       "court_map.txt"};

std::vector<std::string> search_files = {"single_search_map.txt", "duplicate_search_map.txt"};

std::vector<std::string>* files[3] = {&graph_files, &map_files, &search_files};

const int inf = 5;
std::string default_edge = "-1";

//#args: case, loco, time, person, inst, gender, ethic, social, lawyer, lawfirm, lawyernum, lawworker, court
std::vector<int> banned_files = {0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0}; //类初始化的时候就要设定
std::vector<int> banned_nodes = {inf, 0, 0, inf, inf, inf, 0, 0, 0, 0};
//args: case, loco, time, inst, person, lawyer, lawfirm, lawyernum, lawworker, court, attr
//最大单节点扫描数，可设置

std::map<std::string,std::string> nodes_graph;
std::map<std::string,std::string> nodes_map;
std::map<std::string,std::string> search_map;
std::map<std::string,std::string>* structures[3] = {&nodes_graph, &nodes_map, &search_map};

void split(std::vector<std::string>& items, std::string& str, char token) {
    int j = 0;
    int len = str.length();
    for(int i = 0; i < len; i++) {
        if(str[i] == token) {
            items.push_back(str.substr(j, i - j));
            j = i + 1;
        }
    }
    items.push_back(str.substr(j, len - j));
}

//#args: case, loco, time, person, inst, gender, ethic, social, lawyer, lawfirm, lawyernum, lawworker, court
void load(int mode, std::vector<int> args = std::vector<int>(banned_files)) {
/**
# 相等关系   0      0~1，概率
# 当事关系   1      0 原告 1 被告 2 律师 3 代表人 4 代理人 5 审判长 6 审判员 7 法院
# 诉讼关系   2      0 被诉 1 起诉
# 辩护关系   3      0 被辩护 1 辩护
# 代表关系   4      0 被代表 1 代表 2 被委托（代理） 3 委托（被代理）
# 法院关系   5      0 审判长 1 审判员
# 地点关系   6      0 住所地 1 出生地 2 户籍地
# 时间关系   7      0 出生日期 1 判决日期
# 属性关系   8      0 性别 1 民族 2 机构社会编号 3 律所 4 律师执业证号
**/
    std::ifstream file;
    std::string fname;
    std::map<std::string,std::string>* structure = structures[mode];
    std::vector<std::string>* fnames = files[mode];

    for(int i = 0; i < files_len[mode]; i++){
        if (mode == 2 || args[i] == 0) {
            fname = (*fnames)[i];
            file.open(path + fname, std::ifstream::in);
            if (file.is_open()){
                std::cout << fname + " is open\n";
            }
            std::string line;
            std::getline(file, line);
            while(std::getline(file, line) && line != "\n") {
                //std::cout << line << std::endl;
                std::vector<std::string>items;
                split(items, line, '&');
                std::vector<std::string>::iterator iter = items.begin();
                //std::cout << (*iter).c_str() << "----" << (*(iter+1)).c_str() << std::endl;
                structure->insert(std::pair<std::string,std::string>((*iter), (*(iter+1))));
            }
            file.close();
            std::cout << "Successfully loaded " + fname + "\n";
        }
    }
    std::cout << "Successfully loaded all graphs/maps\n";
    return;
}

std::string get_name(std::string id){
    std::map<std::string,std::string>::iterator it = nodes_map.find(id);
    if(it != nodes_map.end()){
        return nodes_map[id];
    }
    return "NULL";
}

/**
# mode 模式 by_step 查询与该节点n步距离内的所有节点，n由distance参数给出
# by_case 查询与该节点相关的案件，并且给出与该案件相关的所有节点
# 默认不对地区（1），时间（2），法院（8），属性（9）做高于一次的跳转（即只能到达该节点，不得从该节点出发）
# 如果需要跳转，则要手动指定打开哪些跳转机制并且限定跳转涉及的节点数，即不能遍历所有节点
# 可以手动设置任何一种节点的最多遍历个数
# 案件（0），地区（1），时间（2），机构（3），当事人（4），律师（5），律所（6），法务（7），法院（8），属性（9）
# kwargs: case, loco, time, inst, person, lawyer, lawfirm, lawworker, court, attr
 * @return
 */

std::vector<std::vector<std::string>> query(std::string id, std::string mode = "by_step", int distance = 1, std::vector<int> args = std::vector<int>(banned_nodes)){
    std::vector<std::vector<std::string>> result(distance + 1);
    /**
    #数字代表允许访问的节点个数
    # 案件（0），地区（1），时间（2），机构（3），当事人（4），律师（5），律所（6），法务（7），法院（8），属性（9）
    **/
    //#根据用户开放的选项设置准许名单

    if(args.end() - args.begin() != 10){
        return result;
    }

    //std::cout << "args is " << args[1] << std::endl;
    std::vector<std::string> worked_nodes;
    std::vector<std::string> working_nodes = {id};
    std::vector<std::string> tmp_nodes;

    std::map<std::string,std::string>::iterator iter = nodes_graph.find(id);

    if(iter != nodes_graph.end() && iter->second != default_edge){
        std::string edge_line = iter->second;
        //std::cout << edge_line << std::endl;
        result[0].push_back(id + " " + edge_line);
        if(mode == "by_step"){
            for(int step = 0; step < distance; step++){
                //std::cout << "step is " << step << std::endl;
                for(std::vector<std::string>::iterator node = working_nodes.begin(); node != working_nodes.end(); node++){
                    if(std::count(worked_nodes.begin(), worked_nodes.end(), *node) == 0){
                        iter = nodes_graph.find(*node);
                        if(iter != nodes_graph.end() && iter->second != default_edge){
                            edge_line = iter->second;
                            std::vector<std::string> edges;
                            split(edges, edge_line, ' ');
                            //edges:各条边的集合，形如3_1:1_0，前者是节点，后者是边权值
                            //std::cout << "edge_line is " << edge_line << std::endl;
                            std::vector<std::string>::iterator edgit = edges.begin();
                            for(edgit; edgit != edges.end(); edgit++){
                                std::vector<std::string> edgsplit;
                                split(edgsplit, *edgit, ':');
                                //std::cout << "Working node is " << *edgit << std::endl;
                                if(std::count(tmp_nodes.begin(), tmp_nodes.end(), edgsplit[0]) + std::count(working_nodes.begin(), working_nodes.end(), edgsplit[0]) + std::count(worked_nodes.begin(), worked_nodes.end(), edgsplit[0]) == 0){

                                    iter = nodes_graph.find(edgsplit[0]);
                                    if(iter != nodes_graph.end() && iter->second != default_edge){
                                        std::vector<std::string> indeces;
                                        split(indeces, edgsplit[0], '_');
                                        int index = std::stoi(indeces[0]);
                                        //std::cout << "step is " << step << std::endl;
                                        //std::cout << "index is " << index << std::endl;
                                        //std::cout << "args[index] is " << args[index] << std::endl;
                                        if(args[index] > 0){
                                            tmp_nodes.push_back(edgsplit[0]);
                                            args[index]--;

                                            //std::cout << "We find " << edgsplit[0] << "----" << iter->first << std::endl;
                                            result[step+1].push_back(iter->first + " " + iter->second);
                                            //std::cout << "output is " << iter->first + "&" + iter->second << std::endl;
                                        }else{
                                            //将不再继续搜寻的节点的边部分置为一个特殊值default_edge
                                            result[step+1].push_back(iter->first + " " + default_edge);
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
                worked_nodes.insert(worked_nodes.end(), working_nodes.begin(), working_nodes.end());
                working_nodes = tmp_nodes;
                tmp_nodes = {};
            }
        }
    }
    return result;
}

std::string search_result(int group, std::string id, std::string mode = "by_step", int step = 1, std::vector<int> node_args = std::vector<int>(banned_nodes)){
    std::vector<std::vector<std::string>> query_result = query(id, mode, step, node_args);
    std::cout << "Search finished. Now constructing graph...\n";
    std::vector<std::vector<std::string>>::iterator qiter = query_result.begin();

    if(qiter != query_result.end()){
        //int cur_group = 0;
        std::string js = "";
        for(int i = 0; i < step + 1; i++){
            /**
            if(i != 0){
                cur_group = group;
            }
             **/
            std::vector<std::string> layer = *(qiter + i);
            std::vector<std::string> layer_next;
            if(i < step){
                //std::cout << "i < step " << std::endl;
                layer_next = *(qiter + (i + 1));
            }else {
                layer_next = {};
            }
            int len_layer = layer.end() - layer.begin();
            //std::cout << "len_layer is" << len_layer << std::endl;
            int len_layer_next = layer_next.end() - layer_next.begin();
            //std::cout << "len_layer_next is" << len_layer_next << std::endl;
            for(int j = 0; j < len_layer; j++){
                std::vector<std::string> info;
                split(info, layer[j], ' ');
                //std::cout << "layer[j] is " << layer[j] << std::endl;
                std::string id = info[0];
                std::string name = get_name(id);
                std::vector<std::string>edges;
                edges.insert(edges.end(), info.begin()+1, info.end());
                //std::cout << "edges are " << edges[0] << std::endl;
                if(edges[0] == "-1"){
                    continue;
                }
                for(int k = j + 1; k < len_layer; k++){
                    //std::cout << "layer[k] is " << layer[k] << std::endl;
                    info.clear();
                    split(info, layer[k], ' ');
                    std::string tar_id = info[0];
                    if(edges[0] == "-1"){
                        continue;
                    }
                    std::string tar_name = get_name(tar_id);
                    //std::cout << "tar_id is " << tar_id << "  tar_name is " << tar_name << std::endl;
                    std::vector<std::string>::iterator eit = edges.begin();
                    while(eit != edges.end()){
                        //std::cout << "eit is " << *eit << std::endl;
                        std::vector<std::string>items;
                        std::vector<std::string>indeces;
                        split(items, *eit, ':');
                        if(tar_id == items[0]){
                            split(indeces, items[1], '_');
                            //std::cout << indeces[0] << "  " << indeces[1] << std::endl;
                            js += "{source:\"" + name + "\", source_id:\"" + id + "\", target:\"" + tar_name + "\", target_id:\"" + tar_id + "\", rela:\"" + edge_matrix[std::stoi(indeces[0])][std::stoi(indeces[1])] + "\", edge_color:" + indeces[0] + ", group:" + std::to_string(group) + "}, ";
                        }
                        eit++;
                    }
                }
                for(int l = 0; l < len_layer_next; l++){
                    info.clear();
                    //std::cout << "layer_next[l] is " << layer_next[l] << std::endl;
                    split(info, layer_next[l], ' ');
                    std::string tar_id = info[0];
                    //std::cout << "tar_id is " << tar_id <<std::endl;
                    if(edges[0] == "-1"){
                        continue;
                    }
                    std::string tar_name = get_name(tar_id);
                    std::vector<std::string>::iterator eit = edges.begin();
                    while(eit != edges.end()){
                        std::vector<std::string>items;
                        std::vector<std::string>indeces;
                        split(items, *eit, ':');
                        if(tar_id == items[0]){
                            split(indeces, items[1], '_');
                            //std::cout << indeces[0] << "  " << indeces[1] << std::endl;
                            js += "{source:\"" + name + "\", source_id:\"" + id + "\", target:\"" + tar_name + "\", target_id:\"" + tar_id + "\", rela:\"" + edge_matrix[std::stoi(indeces[0])][std::stoi(indeces[1])] + "\", edge_color:" + indeces[0] + ", group:" + std::to_string(group) + "}, ";
                        }
                        eit++;
                    }
                }

            }
        }
        //std::cout << "js is " << js << std::endl;
        //std::cout << "graph is " << '[' + js + ']' << std::endl;
        return js;
    }
    return "";
}

std::vector<std::string> search_id(std::string name){
    std::vector<std::string> ids = {};
    std::map<std::string,std::string>::iterator iter = search_map.find(name);
    if (iter != search_map.end()){
        std::cout << iter->second << std::endl;
        split(ids, iter->second, ' ');
    }else{
        std::cout << "No such keyword!\n";
    }
    return ids;
}

int main(){
    load(0);
    load(1);
    load(2);
    //std::cout << nodes_graph["3_451"] << std::endl;

    std::ofstream of;
    of.open("out.txt", std::ofstream::out);
    //#args: case, loco, time, person, inst, gender, ethic, social, lawyer, lawfirm, lawyernum, lawworker, court
    std::vector<int>args = {inf, 0, 0, inf, inf, inf, 0, 0, 0, 0};
    std::string id;
    std::string quest;
    std::string result;
    std::cout << "Search for id, please enter 0.\nSearch for graph by id, please enter 1.\nSearch for graph by name, please enter 2.\nTo exit, enter -1.\n";
    std::cin >> id;
    while(id != "-1"){
        if(id == "0"){
            std::cout << "Please enter keyword.\n";
            std::cin >> quest;
            search_id(quest);
        }
        else if(id == "1") {
            std::cout << "Please enter id.\n";
            std::cin >> quest;
            result = search_result(0, quest, "by_step", 2, args);
            if(result.length() > 2) {
                result.pop_back();
                result.pop_back();
            }
            result = "[" + result + "]";
            std::cout << result << std::endl;
            of << result << std::endl;
        }
        else if(id == "2") {
            std::cout << "Please enter keyword.\n";
            std::cin >> quest;
            std::vector<std::string> ids = search_id(quest);
            std::vector<std::string>::iterator idit = ids.begin();
            int group = 0;
            while(idit != ids.end()){
                result += search_result(group, *idit, "by_step", 2, args);
                group++;
                idit++;
            }
            if(result.length() > 2) {
                result.pop_back();
                result.pop_back();
            }
            result = "[" + result + "]";
            std::cout << result << std::endl;
            of << result << std::endl;
        }else{
            std::cout << "Wrong quest!\n";
        }
        result = "";
        std::cout << "Search for id, please enter 0.\nSearch for graph by id, please enter 1.\nSearch for graph by name, please enter 2.\nTo exit, enter -1.\n";
        std::cin >> id;
    }

    //std::cout << nodes_graph.begin()->first << "   " << nodes_graph.begin()->second << std::endl;
    /**
    std::vector<std::vector<std::string>> result = query("0_1");
    std::vector<std::vector<std::string>>::iterator fiter = result.begin();
    while(fiter != result.end()){
        std::vector<std::string>::iterator siter = fiter->begin();
        while(siter != fiter->end()){
            std::cout << *siter << std::endl;
            siter++;
        }
        fiter++;
    }
    **/
    of.close();
    return 0;
}