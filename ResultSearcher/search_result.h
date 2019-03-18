#ifndef SEARCH_RESULT_H
#define SEARCH_RESULT_H

class Searcher{
protected:

    static const int inf = 5;
    static const int files_len = 13;
    static const std::string default_edge = "-1";

    static const std::string edge_matrix[9][8];
    static const std::vector<std::string> graph_files;
    static const std::vector<std::string> map_files;

    static std::vector<int> banned_files; //类初始化的时候就要设定
    static std::vector<int> banned_nodes;
    static std::map<std::string,std::string> nodes_graph;
    static std::map<std::string,std::string> nodes_map;
    static std::map<std::string,std::string>* structures[2];

    void split(std::vector<std::string>&, std::string&, char);
    std::string get_name(std::string);
    void set_banned_files(std::vector<int>);
    void load(int, std::vector<int> args = std::vector<int>(banned_files));

public:
    Searcher();
    Searcher(std::vector<int>);
    std::vector< std::vector<std::string> > query(std::string, std::string mode = "by_step", int distance = 1, std::vector<int> args = std::vector<int>(banned_nodes));
    void search_result(std::string, std::ofstream* f, std::string mode = "by_step", int step = 1, std::vector<int> node_args = std::vector<int>(banned_nodes));
};

#endif