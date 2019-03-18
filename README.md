# Legal-Document-Knowledge-Graph-Generator
This is the research project at NLP Lab of Tsinghua University.<br><br>

DocumentParser is for preprocessing raw documents into clean, structurized texts. Follow the numbers in the file names and the scripts will automatically store the preprocessed data.<br><br>

KnowledgeGraphBuilder is for mapping the preprocessed data into a dictionary-style directed graph of entities and relations. To speed up the building process the core component is written in C++ for efficiency, while the script is in Python for ease of use. The package will also create commonly used indexes.<br><br>

ResultSearcher is a web search interface. It's based on Flask, SQLite, Sphinx and d3.js. By running the Flask backend and Sphinx Chinese search engine, one can easily retrieve the entities related to a certain key word and see the relations between them with an interactive d3.js force graph.

![image](https://github.com/zhangyuwangumass/Legal-Document-Knowledge-Graph-Generator/master/search_graph.png)
