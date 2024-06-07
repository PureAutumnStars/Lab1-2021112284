"""
软件工程实验三 代码评审与单元测试 Python=3.9
Lab1 引用部分
2021110522 苗梓萌
2021112284 王梓健
2024/06
"""
TEST_FILE_PATH = "./data/test/origin.txt"


def Get_Word_List_from_Nodes(node_list):
    """
    从结点列表中获取词表
    """
    word_list = []
    for i in range(len(list(node_list.keys()))):
        word_list.append(node_list[i].name)
    return word_list


def queryBridgeWords(G, word1, word2):
    """
    查询桥接词
    """
    bridge = []
    word_list = Get_Word_List_from_Nodes(G)
    if word1 not in word_list and word2 not in word_list:
        result_string = f"查询失败: No \"{word1}\" and \"{word2}\" in the graph!"
        print(result_string)
        return bridge, result_string
    elif word1 not in word_list:
        result_string = f"查询失败: No \"{word1}\" in the graph!"
        print(result_string)
        return bridge, result_string
    elif word2 not in word_list:
        result_string = f"查询失败: No \"{word2}\" in the graph!"
        print(result_string)
        return bridge, result_string
    index1 = word_list.index(word1)
    index2 = word_list.index(word2)
    nodelist = G
    node1 = nodelist[index1]
    node2 = nodelist[index2]
    bridge = set(node1.after.keys()).intersection(set(node2.before.keys()))
    bridge = list(bridge)
    bridge = [word_list[p] for p in bridge]
    if len(bridge) == 0:
        result_string = f"查询成功: No bridge word from \"{word1}\" to \"{word2}\"!"
        print(result_string)
    elif len(bridge) == 1:
        result_string = f"查询成功: The bridge word from \"{word1}\" to \"{word2}\" is: {bridge[0]}."
        print(result_string)
    else:
        word_string = ""
        for i in range(0, len(bridge) - 1):
            word_string = word_string + bridge[i] + ", "
        word_string = word_string[:-2] + " and " + bridge[len(bridge) - 1]
        result_string = f"查询成功: The bridge words from \"{word1}\" to \"{word2}\" are: {word_string}."
        print(result_string)
    return bridge, result_string


def input_query():
    """
    桥接词查询提示输入信息
    """
    prompt = input("请输入待查询的桥接词：\n")
    words = prompt.split()
    if len(words) != 2:
        print("\n输入格式错误，退出程序")
        exit(0)
    else:
        word_1 = words[0].lower()
        word_2 = words[1].lower()
    return word_1, word_2
