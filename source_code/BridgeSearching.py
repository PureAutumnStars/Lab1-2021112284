"""
Lab 1 桥接词部分
"""

import matplotlib.pyplot as plt
import networkx as nx
import os


def showBridgeOnGraph(G, pos, path, k1, k2, bridge):
    """
    展示标注桥接词后的图
    :param G: 初始化后的带权有向图
    :param pos: 节点位置
    :param path: 程序保存图像的路径，常量不变
    :param k1: 桥接词前项
    :param k2: 桥接词后项
    :param bridge: 桥接词列表
    """
    dir_path = os.path.join(path, "BridgeQuery")
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)
    for word in bridge:
        bridge_dir = os.path.join(dir_path, f"{k1}-{k2}")
        if not os.path.isdir(bridge_dir):
            os.makedirs(bridge_dir)

        plt.rcParams['figure.figsize'] = (12, 15)
        nx.draw(G, pos, alpha=0.5, node_size=700)
        node_labels = nx.get_node_attributes(G, 'name')
        nx.draw_networkx_labels(G, pos=pos, labels=node_labels, font_size=7)

        edge_pairs_bridge = [(k1, word), (word, k2)]
        nx.draw_networkx_edges(G, pos, edgelist=edge_pairs_bridge, edge_color='m', width=4)
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

        plt.savefig(os.path.join(bridge_dir, f"{k1}-{word}-{k2}.png"))
        plt.show()


def printInfo(s, flag):
    """
    展示标注桥接词后的图
    :param s: 待打印的错误信息
    :param flag: 标志变量，是否需要打印错误信息
    """
    if flag:
        print(s)


def input_query():
    """
    提示信息，接收待查桥接词的前项与后项
    :return word1: 桥接词前项
    :return word2: 桥接词后项
    """
    prompt = input("-------依次输入桥接词前后项，用空格隔开-------\n")
    prompt = prompt.split()
    if len(prompt) == 2:
        return prompt[0].lower(), prompt[1].lower()
    else:
        print("\n-------待查query输入有误, 已退出程序-------\n")
        exit(0)


def input_insert():
    """
    提示信息：输入需要插入桥接词的句子
    :return: sentence: 输入的句子
    """
    prompt = input("-------向句子中插入桥接词，原句子提示输入，键入A进入备选句子选择，键入B输入自定义句子-------\n")
    if prompt == "A":
        print("-----备选文件如下所示-----")
        path = "./data/bridge_word_insert/input"
        file_list = os.listdir(path)
        names = []
        for file in file_list:
            file_name = file.split("/")[-1]
            names.append(file_name)
            print(f"{file_name}\n")
        choose = input("-----请输入选择的文件名，需要带后缀名-----\n")
        while choose not in names:
            print("-----输入的文件名不在备选中，请重新输入！-----\n")
            choose = input()
        file = path + "/" + choose
        with open(file, "r", encoding="utf-8") as f:
            sentence = f.read()

    elif prompt == "B":
        sentence = input("-----请输入自定义句子-----\n")

    else:
        print("错误键入，退出程序！")
        exit(0)

    print(f"-----您输入的句子是：{sentence} -----")

    return sentence
