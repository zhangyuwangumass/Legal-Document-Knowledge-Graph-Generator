#include "search_result.h"
#include <fstream>

int main(){
    std::ofstream of("result.txt", std::ios::out);
    Searcher searcher = Searcher();
    searcher.search_result("3_592", &of, "by_step", 2);
}