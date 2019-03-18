#include "search_result.h"
#include <iostream>
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

void Searcher::split(std::vector<std::string>& items, std::string& str, char token) {
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

std::string Searcher::get_name(std::string id){
    std::map<std::string,std::string>::iterator it = nodes_map.find(id);
    if(it != nodes_map.end()){
        return nodes_map[id];
    }
    return "NULL";
}

void Searcher::set_banned_files(std::vector<int> banned_files){
    if(banned_files.end() - banned_files.begin() == 13){this->banned_files = banned_files;}
}

//#args: case, loco, time, person, inst, gender, ethic, social, lawyer, lawfirm, lawyernum, lawworker, court
void Searcher::load(int mode, std::vector<int> args = std::vector<int>(banned_files)) {
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

    for(int i = 0; i < files_len; i++){
        if (args[i] == 0) {
            fname = (*fnames)[i];
            file.open(fname, std::ifstream::in);
            if (file.is_open()){
                std::cout << fname + " is open\n";
            }
            std::string line;
            while(std::getline(file, line) && line != "\n") {
                std::vector<std::string>items;
                split(items, line, '&');
                std::vector<std::string>::iterator iter = items.begin();
                structure->insert(std::pair<std::string,std::string>((*iter), (*(iter+1))));
            }
            file.close();
            std::cout << "Successfully loaded " + fname + "\n";
        }
    }
    std::cout << "Successfully loaded all graphs/maps\n";
}

Searcher::Searcher(){
    edge_matrix[9][8] = {{"NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL","NULL"},
        {"当事人", "当事人", "律师", "代表人", "代理人", "审判长", "审判员", "法院"},
        {"被诉", "起诉", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL"},
        {"被辩护", "辩护", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL"},
        {"被代表", "代表", "委托（被代理）", "被委托（代理）", "NULL", "NULL", "NULL", "NULL"},
        {"审判长", "审判员", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL"},
        {"住所地", "出生地", "户籍地", "NULL", "NULL", "NULL", "NULL", "NULL"},
        {"出生日期", "判决日期", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL"},
        {"性别", "民族", "机构社会编号", "律所", "律师执业证号", "NULL", "NULL", "NULL"}};

    graph_files = {"case_graph.txt", "loco_graph.txt",
                "time_graph.txt", "person_graph.txt",
                "inst_graph.txt", "gender_graph.txt",
                "ethic_graph.txt", "social_graph.txt",
                "lawyer_graph.txt", "lawfirm_graph.txt",
                "lawyernum_graph.txt", "lawworker_graph.txt",
                "court_graph.txt"};

    map_files = {"case_map.txt", "loco_map.txt",
                                                     "time_map.txt", "person_map.txt",
                                                     "inst_map.txt", "gender_map.txt",
                                                     "ethic_map.txt", "social_map.txt",
                                                     "lawyer_map.txt", "lawfirm_map.txt",
                                                     "lawyernum_map.txt", "lawworker_map.txt",
                                                     "court_map.txt"};

    banned_files = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}; //类初始化的时候就要设定
    banned_nodes = {inf, 0, 0, inf, inf, inf, 0, 0, 0, 0};
    structures[2] = {&nodes_graph, &nodes_map};

    load(0);
    load(1);
}

Searcher::Searcher(std::vector<int> files){
    Searcher();
    set_banned_files(files);
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

std::vector< std::vector<std::string> > Searcher::query(std::string id, std::string mode = "by_step", int distance = 1, std::vector<int> args = std::vector<int>(banned_nodes)){
    std::vector< std::vector<std::string> > result(distance + 1);
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
        result[0].push_back(id + " " + edge_line);
        if(mode == "by_step"){
            for(int step = 0; step < distance; step++){
                for(std::vector<std::string>::iterator node = working_nodes.begin(); node != working_nodes.end(); node++){
                    if(std::count(worked_nodes.begin(), worked_nodes.end(), *node) == 0){
                        iter = nodes_graph.find(*node);
                        if(iter != nodes_graph.end() && iter->second != default_edge){
                            edge_line = iter->second;
                            std::vector<std::string> edges;
                            split(edges, edge_line, ' ');
                            std::vector<std::string>::iterator edgit = edges.begin();
                            for(edgit; edgit != edges.end(); edgit++){
                                std::vector<std::string> edgsplit;
                                split(edgsplit, *edgit, ':');
                                if(std::count(tmp_nodes.begin(), tmp_nodes.end(), edgsplit[0]) + std::count(working_nodes.begin(), working_nodes.end(), edgsplit[0]) + std::count(worked_nodes.begin(), worked_nodes.end(), edgsplit[0]) == 0){

                                    iter = nodes_graph.find(edgsplit[0]);
                                    if(iter != nodes_graph.end() && iter->second != default_edge){
                                        std::vector<std::string> indeces;
                                        split(indeces, edgsplit[0], '_');
                                        int index = std::stoi(indeces[0]);
                                        if(args[index] > 0){
                                            tmp_nodes.push_back(edgsplit[0]);
                                            args[index]--;
                                            result[step+1].push_back(iter->first + " " + iter->second);
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

void Searcher::search_result(std::string id, std::ofstream* f, std::string mode = "by_step", int step = 1, std::vector<int> node_args = std::vector<int>(banned_nodes)){
    std::vector< std::vector<std::string> > query_result = query(id, mode, step, node_args);
    std::cout << "Search finished. Now constructing graph...\n";
    std::vector<std::vector<std::string>>::iterator qiter = query_result.begin();
    if(qiter != query_result.end()){
        std::string js = "";
        for(int i = 0; i < step + 1; i++){
            std::vector<std::string> layer = *(qiter + i);
            std::vector<std::string> layer_next;
            if(i < step){
                layer_next = *(qiter + (i + 1));
            }else {
                layer_next = {};
            }
            int len_layer = layer.end() - layer.begin();
            int len_layer_next = layer_next.end() - layer_next.begin();
            for(int j = 0; j < len_layer; j++){
                std::vector<std::string> info;
                split(info, layer[j], ' ');
                std::string id = info[0];
                std::string name = get_name(id);
                std::vector<std::string>edges;
                edges.insert(edges.end(), info.begin()+1, info.end());
                if(edges[0] == "-1"){
                    continue;
                }
                for(int k = j + 1; k < len_layer; k++){
                    info.clear();
                    split(info, layer[k], ' ');
                    std::string tar_id = info[0];
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
                            js += "{source:\"" + name + "\", target:\"" + tar_name + "\", rela:\"" + edge_matrix[std::stoi(indeces[0])][std::stoi(indeces[1])] + "\", edge_color:" + indeces[0] + ", type:\"resolved\"}, ";
                        }
                        eit++;
                    }
                }
                for(int l = 0; l < len_layer_next; l++){
                    info.clear();
                    split(info, layer_next[l], ' ');
                    std::string tar_id = info[0];
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
                            js += "{source:\"" + name + "\", target:\"" + tar_name + "\", rela:\"" + edge_matrix[std::stoi(indeces[0])][std::stoi(indeces[1])] + "\", edge_color:" + indeces[0] + ", type:\"resolved\"}, ";
                        }
                        eit++;
                    }
                }

            }
        }
        js.pop_back();
        js.pop_back();
        std::cout << "js is " << js << std::endl;
        *f << '[' + js + ']';
    }
}