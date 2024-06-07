import unittest
from BackendUtils import *
from DataProcessing import *

_, _, G = text_to_graph(TEST_FILE_PATH)


class Test_queryBridgeWords(unittest.TestCase):
    def test_path_1(self):
        word_1 = "not"  # 原文中有的词
        word_2 = "you"  # 原文中有的词
        word_1 = word_1.lower()
        word_2 = word_2.lower()
        expected_output = f"查询成功: The bridge words from \"{word_1}\" to \"{word_2}\" are: believe and only."
        _, output = queryBridgeWords(G, word_1, word_2)
        self.assertEqual(output, expected_output)

    def test_path_2(self):
        word_1 = "will"  # 原文中有的词
        word_2 = "trust"  # 原文中有的词
        word_1 = word_1.lower()
        word_2 = word_2.lower()
        expected_output = f"查询成功: The bridge word from \"{word_1}\" to \"{word_2}\" is: never."
        _, output = queryBridgeWords(G, word_1, word_2)
        self.assertEqual(output, expected_output)

    def test_path_3(self):
        word_1 = "do"  # 原文中有的词
        word_2 = "I"  # 原文中有的词
        word_1 = word_1.lower()
        word_2 = word_2.lower()
        expected_output = f"查询成功: No bridge word from \"{word_1}\" to \"{word_2}\"!"
        _, output = queryBridgeWords(G, word_1, word_2)
        self.assertEqual(output, expected_output)

    def test_path_4(self):
        word_1 = "not"  # 原文中有的词
        word_2 = "extraordinary"  # 原文中没有的词
        word_1 = word_1.lower()
        word_2 = word_2.lower()
        expected_output = f"查询失败: No \"{word_2}\" in the graph!"
        _, output = queryBridgeWords(G, word_1, word_2)
        self.assertEqual(output, expected_output)

    def test_path_5(self):
        word_1 = "encyclopedia"  # 原文中没有的词
        word_2 = "you"  # 原文中有的词
        word_1 = word_1.lower()
        word_2 = word_2.lower()
        expected_output = f"查询失败: No \"{word_1}\" in the graph!"
        _, output = queryBridgeWords(G, word_1, word_2)
        self.assertEqual(output, expected_output)

    def test_path_6(self):
        word_1 = "encyclopedia"  # 原文中没有的词
        word_2 = "extraordinary"  # 原文中没有的词
        word_1 = word_1.lower()
        word_2 = word_2.lower()
        expected_output = f"查询失败: No \"{word_1}\" and \"{word_2}\" in the graph!"
        _, output = queryBridgeWords(G, word_1, word_2)
        self.assertEqual(output, expected_output)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTests([Test_queryBridgeWords("test_path_1"), Test_queryBridgeWords("test_path_2"),
                  Test_queryBridgeWords("test_path_3"), Test_queryBridgeWords("test_path_4"),
                  Test_queryBridgeWords("test_path_5"), Test_queryBridgeWords("test_path_6")])
    runner = unittest.TextTestRunner()
    runner.run(suite)
