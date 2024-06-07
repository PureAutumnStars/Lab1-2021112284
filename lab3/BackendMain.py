"""
软件工程实验三 代码评审与单元测试 Python=3.9
Lab1 主函数部分
2021110522 苗梓萌
2021112284 王梓健
2024/06
"""
from DataProcessing import *
from BackendUtils import *

if __name__ == "__main__":
    nx_graph, word_list, G = text_to_graph(TEST_FILE_PATH)

    word_1, word_2 = input_query()

    queryBridgeWords(G, word_1, word_2)
