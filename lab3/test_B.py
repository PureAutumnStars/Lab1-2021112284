import pytest
from BackendUtils import *
from DataProcessing import *

_, _, G = text_to_graph(TEST_FILE_PATH)


class Test_queryBridgeWords:
    def test_1(self):
        word_1 = "encyclopedia"  # 原文中没有的词
        word_2 = "extraordinary"  # 原文中没有的词
        word_1 = word_1.lower()
        word_2 = word_2.lower()
        expected_output = f"查询失败: No \"{word_1}\" and \"{word_2}\" in the graph!"
        _, output = queryBridgeWords(G, word_1, word_2)
        assert output == expected_output

    def test_2(self):
        word_1 = "encyclopedia"  # 原文中没有的词
        word_2 = "you"  # 原文中有的词
        word_1 = word_1.lower()
        word_2 = word_2.lower()
        expected_output = f"查询失败: No \"{word_1}\" in the graph!"
        _, output = queryBridgeWords(G, word_1, word_2)
        assert output == expected_output

    def test_3(self):
        word_1 = "not"  # 原文中有的词
        word_2 = "extraordinary"  # 原文中没有的词
        word_1 = word_1.lower()
        word_2 = word_2.lower()
        expected_output = f"查询失败: No \"{word_2}\" in the graph!"
        _, output = queryBridgeWords(G, word_1, word_2)
        assert output == expected_output

    def test_4(self):
        """
        待查询词在原文中均有，但无桥接词的情况
        """
        word_1 = "do"  # 原文中有的词
        word_2 = "I"  # 原文中有的词
        word_1 = word_1.lower()
        word_2 = word_2.lower()
        expected_output = f"查询成功: No bridge word from \"{word_1}\" to \"{word_2}\"!"
        _, output = queryBridgeWords(G, word_1, word_2)
        assert output == expected_output

    def test_5(self):
        """
        待查询词在原文中均有，只有一个 桥接词的情况
        """
        word_1 = "will"  # 原文中有的词
        word_2 = "trust"  # 原文中有的词
        word_1 = word_1.lower()
        word_2 = word_2.lower()
        expected_output = f"查询成功: The bridge word from \"{word_1}\" to \"{word_2}\" is: never."
        _, output = queryBridgeWords(G, word_1, word_2)
        assert output == expected_output

    def test_6(self):
        """
        待查询词在原文中均有，有多个 桥接词的情况
        """
        word_1 = "not"  # 原文中有的词
        word_2 = "you"  # 原文中有的词
        word_1 = word_1.lower()
        word_2 = word_2.lower()
        expected_output = f"查询成功: The bridge words from \"{word_1}\" to \"{word_2}\" are: believe and only."
        _, output = queryBridgeWords(G, word_1, word_2)
        assert output == expected_output
