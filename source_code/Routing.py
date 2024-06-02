"""
Lab 1 路由部分
"""
import random
from time import sleep
import numpy as np

INF = 9999


def input_shortest_path(G):
    """
    提示信息，选择需要查询最短路径的两结点
    :param: G: 调用 nx.DiGraph() 构造的带权有向图
    :return: word_1: 起始结点的名，即存储的单词
    :return: word_2: 结束结点的名，即存储的单词
    """
    nodes_name = list(G.nodes())
    print("-----根据输入构造的图的结点列表如下-----")
    print(nodes_name)
    prompt = input("-------请选择待查询最短路径的两个单词，用空格隔开-------\n")
    prompt = prompt.split()
    if len(prompt) == 2:
        return prompt[0].lower(), prompt[1].lower()
    else:
        print("\n-------待查两单词输入有误, 已退出程序-------\n")
        exit(0)


class Graph:
    def __init__(self, n):
        self.vertexn = n
        self.gType = 0
        self.vertexes = [INF]*n
        self.arcs = [self.vertexes*n]  # 邻接矩阵
        self.visited = [False]*n  # 用于深度遍历记录结点的访问情况

    def addvertex(self, v, i):
        self.vertexes[i] = v

    def addarcs(self, row, column, weight):
        self.arcs[row][column] = weight

    # 最短路径算法-Dijkstra 输入点v0，找到所有点到v0的最短距离
    def Dijkstra(self, v0):
        D = [INF]*self.vertexn  
        path4one = [None]  
        paths = [path4one]*self.vertexn
        final = [None]*self.vertexn
        for i in range(self.vertexn):
            final[i] = False
            D[i] = self.arcs[v0][i]
            if D[i] < INF:
                paths[i] = [v0] 
        D[v0] = 0
        final[v0] = True

        for i in range(1, self.vertexn):
            mini = INF  # 找到离v0最近的顶点
            v = -1
            for k in range(self.vertexn):
                if(not final[k]) and (D[k] < mini):
                    v = k
                    mini = D[k]
            
            if v != -1:
                final[v] = True  # 最近的点找到，加入到已得最短路径集合S中 此后的min将在处S以外的vertex中产生
                for k in range(self.vertexn):
                    if not final[k]: 
                        if mini + self.arcs[v][k] < D[k]:
                            # 如果最短的距离(v0-v)加上v到k的距离小于现存v0到k的距离
                            D[k] = mini + self.arcs[v][k]
                            paths[k] = []
                            paths[k].append(v)
                        elif mini + self.arcs[v][k] == D[k]:
                            paths[k].append(v)
            else:
                break
        
        return D, paths
    
    def getPaths(self, start_seq, end_seq, data):
        """
        从Dijkstra返回的前驱结构中获取单源的最短路径
        :param start_seq: 开始结点的序号
        :param end_seq: 结束结点的序号
        :param data: 前驱数据结构
        :return midPaths: 最短路径
        """
        childPaths = [[]*self.vertexn]
        midPaths = []
        if(end_seq != start_seq):
            for i in range(len(data[end_seq])):
                childPaths = self.getPaths(start_seq, data[end_seq][i], data)
                for j in range(len(childPaths)):
                    childPaths[j].append(end_seq)
                if len(midPaths) == 0:
                    midPaths = childPaths
                else:
                    for elem in childPaths:
                        midPaths.append(elem)
        else:
            midPaths.append([start_seq])
        return midPaths
    
    def getAllPath(self, start_seq, data):
        """
        从Dijkstra返回的前驱结构中获取某一节点到其他节点的最短路径, 多条则选用节点数最小的
        :param start_seq: 开始结点的序号
        :param data: 前驱数据结构
        :return allPaths: 最短路径
        """
        allPaths = []
        for i in range(0, self.vertexn):
            if data[i][0] is not None and i != start_seq:
                path_list = self.getPaths(start_seq, i, data)
                minvertexs = min(path_list, key=len)
                allPaths.append(minvertexs)
            else:
                allPaths.append([])
        return allPaths

def Nodes_to_Matrix(node_list):
    """
    接口型函数：提取Node列表的信息构造图的邻接矩阵表示
    :param node_list: Node列表
    :return: matrix: 图的邻接矩阵表示
    """
    node_num = len(node_list)
    matrix = np.zeros((node_num, node_num))
    for i in range(node_num):
        node = node_list[i]
        seq = node.seq
        after_seqs = node.after.keys()
        for after_seq in after_seqs:
            matrix[seq, after_seq] = node.after[after_seq]
    for i in range(node_num):
        for j in range(node_num):
            if matrix[i, j] == 0:
                matrix[i, j] = INF
    return matrix


def Nodes_to_Graph(node_list):
    """
    接口型函数：从结点列表建图
    :param node_list: Node列表
    :return: G: 用于查询的图
    """
    n = len(node_list)
    G = Graph(n)

    names = []
    for i in range(n):
        names.append(node_list[i].name)
    matrix = Nodes_to_Matrix(node_list)

    G.vertexes = names
    G.arcs = matrix

    return G


def search_word(word, search_list):
    """
    在指定列表中查询指定词的位置
    :param word: 待检索的单词
    :param search_list: 检索列表
    :return: result: 位置列表，列表的元素是该检索的单词在检索列表中的位置
    """
    result = []
    for i in range(len(search_list)):
        if word == search_list[i]:
            result.append(i)
    return result


def if_quit_by_repeated_edge(word_list, addr_list):
    """
    判断是否终止随机游走，条件：出现重复的边
    :param word_list: 当前已游走经过的单词形成的列表
    :param addr_list: 当前词在word_list中的位置形成的列表
    :return: quit_flag: True or False
    """
    front_word_list = []
    quit_flag = False
    if addr_list[0] > 0:
        front_word_list.append(word_list[addr_list[0] - 1])
        for i in range(1, len(addr_list)):
            front_word = word_list[addr_list[i] - 1]
            if front_word in front_word_list:
                quit_flag = True
            else:
                front_word_list.append(front_word)
    elif addr_list[0] == 0 and len(addr_list) > 2:
        front_word_list.append(word_list[addr_list[1] - 1])
        for i in range(2, len(addr_list)):
            front_word = word_list[addr_list[i] - 1]
            if front_word in front_word_list:
                quit_flag = True
            else:
                front_word_list.append(front_word)

    return quit_flag


def Random_Walk(node_list, start_seq, save_path):
    """
    随机游走
    :param node_list: 结点列表
    :param start_seq: 开始结点的序号
    :param save_path: 保存文件的路径
    """
    file = open(save_path, "w", encoding="utf-8")
    word_list = []
    line = str()
    seq = start_seq
    try:
        while len(node_list[seq].after.keys()) >= 0:
            word = node_list[seq].name
            word_list.append(word)

            addr_list = search_word(word, word_list)
            if len(addr_list) > 1:
                quit_flag = if_quit_by_repeated_edge(word_list, addr_list)
                if quit_flag:
                    break

            next_words = list(node_list[seq].after.keys())
            if len(next_words) == 0:
                break
            else:
                rand = random.randint(0, len(next_words) - 1)
                seq = next_words[rand]

            sleep(2)

        print("-------已完成随机游走-------\n")

        for word_i in word_list:
            line += (word_i + " ")
        file.write(line)

    except KeyboardInterrupt:
        print("-------检测到用户行为，中断随机游走-------\n")
        for word_i in word_list:
            line += (word_i + " ")
        file.write(line)



    
    

