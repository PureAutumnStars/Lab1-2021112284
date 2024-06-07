"""
软件工程实验三 代码评审与单元测试 Python=3.9
Lab1 数据处理部分
2021110522 苗梓萌
2021112284 王梓健
2024/06
"""
import re
import string
import networkx as nx

PUNCTUATIONS = string.punctuation  # 英文的标点符号
PATTERN = re.compile(r"[^a-zA-Z]")  # 英文pattern


class Node:
    """
    图的结点
    """
    def __init__(self, name=str, seq=int):
        """
        初始化
        :param name: 词名
        :param seq: 该单词在词表中的序号
        """
        self.name = name
        self.seq = seq
        self.before = {}  # 该单词的前一个词，字典，{序号：边权}
        self.after = {}  # 该单词的后一个词，字典，{序号：边权}

    def add_before(self, seq_before):
        """
        插入前向结点
        :param seq_before: 该单词的前一个词的序号
        """
        if seq_before in self.before.keys():
            self.before[seq_before] += 1
        else:
            self.before[seq_before] = 1

    def add_after(self, seq_after):
        """
        插入后向结点
        :param seq_after: 该单词的下一个词序号
        """
        if seq_after in self.after.keys():
            self.after[seq_after] += 1
        else:
            self.after[seq_after] = 1


def preprocessing(txt):
    """
    预处理文本文件，要求如下：
    1. 将换行符和回车符当作空格
    2. 标点符号作为空格
    3. 忽略非英文字母的字符
    :param txt: 待输入文件的文件路径
    :return: word_list: 满足上述要求的文本按空格切分的词列表
    """
    f = open(txt, "r", encoding="utf-8")
    file = f.read().lower()  # str，大写转为小写
    file = re.sub(r"\n", " ", file, flags=re.IGNORECASE)  # 换行符/回车替换为空格
    for punctuation in PUNCTUATIONS:
        file = file.replace(punctuation, " ")  # 标点符号替换为空格
    file = re.sub(PATTERN, " ", file)  # 去除非英文符号
    word_list = file.split()
    return word_list


def text_to_graph(txt):
    """
    读入文本并转换为有向图
    :param txt: 输入文本的路径
    :return: G，有向图的结点字典，{序号：结点类}  * 待完善
    :return: words: 去重后的词表
    :return: node_list: 节点列表数据结构
    """
    node_list = {}
    # 预处理
    word_list = preprocessing(txt)
    # 获取去重后的词表
    words = []
    for i in word_list:
        if i not in words:
            words.append(i)
    # 遍历处理后的文本
    for i in range(len(word_list)):
        word = word_list[i]
        seq = words.index(word)

        if seq not in node_list.keys():
            node_list[seq] = Node(name=word, seq=seq)  # 新建结点并插入结点字典
        if i > 0:
            seq_before = words.index(word_list[i-1])
            node_list[seq].add_before(seq_before)
        if i < len(word_list)-1:
            seq_after = words.index(word_list[i+1])
            node_list[seq].add_after(seq_after)

    G = nx.DiGraph()
    for index in node_list.keys():
        G.add_node(words[index], name=words[index])
    for index in node_list.keys():
        n = node_list[index]
        for target in n.before.keys():
            G.add_edge(words[target], words[index], weight=n.before[target])
        for target in n.after.keys():
            G.add_edge(words[index], words[target], weight=n.after[target])
    return G, words, node_list
