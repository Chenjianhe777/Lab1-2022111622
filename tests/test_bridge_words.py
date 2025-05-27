import unittest
import sys
import os

# 添加 src 目录到模块搜索路径
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))
sys.path.append(src_path)

from word_graph import build_graph, queryBridgeWords
from word_graph import graph as module_graph

class TestBridgeWords(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 初始化测试图
        test_data_dir = os.path.join(os.path.dirname(__file__), "../test_data")
        test_file = os.path.join(test_data_dir, "test_text.txt")
        cls.test_graph = build_graph(test_file)
        global module_graph
        module_graph = cls.test_graph

    def test_valid_bridge_words(self):
        result = queryBridgeWords("team", "more")
        expected_words = ["requested"]
        for word in expected_words:
            self.assertIn(word, result)

    def test_missing_word2(self):
        result = queryBridgeWords("data", "apple")
        self.assertIn( "No apple in the graph!", result)

    def test_no_bridge_words(self):
        result = queryBridgeWords("data", "report")
        self.assertIn("No bridge words from data to report!", result)

    def test_invalid_input(self):
        result = queryBridgeWords("apple", "banana")
        self.assertIn("No apple and banana in the graph!", result)

    def test_graph_loaded(self):
        self.assertIsNotNone(module_graph)
        self.assertGreater(len(module_graph.nodes), 0)

if __name__ == '__main__':
    unittest.main()
