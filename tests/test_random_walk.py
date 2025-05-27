import unittest
from unittest.mock import patch
import sys
import os
import itertools

# 添加 src 目录到模块搜索路径
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))
sys.path.append(src_path)

import word_graph
from word_graph import Graph, randomWalk

class TestRandomWalkWhiteBox(unittest.TestCase):
    def setUp(self):
        self.original_graph = Graph()
        word_graph.graph = self.original_graph  # 关键：显式设置 graph

    def tearDown(self):
        word_graph.graph = None

    def test_empty_graph(self):
        result = randomWalk()
        self.assertEqual(result, "")

    def test_single_node_no_edges(self):
        word_graph.graph.nodes["A"] = {}
        with patch('random.choice') as mock_choice:
            mock_choice.return_value = "A"
            result = randomWalk()
        self.assertEqual(result, "A")

    def test_repeated_edge(self):
        word_graph.graph.nodes["A"] = {"B": 1}
        word_graph.graph.nodes["B"] = {"A": 1}
        with patch('random.choice') as mock_choice:
            mock_choice.side_effect = itertools.cycle(["A", "B"])
            result = randomWalk()
        self.assertEqual(result, "A B A")

    def test_normal_walk(self):
        word_graph.graph.nodes["A"] = {"B": 1}
        word_graph.graph.nodes["B"] = {"C": 1}
        word_graph.graph.nodes["C"] = {}
        with patch('random.choice') as mock_choice:
            mock_choice.side_effect = ["A", "B", "C"]
            result = randomWalk()
        self.assertEqual(result, "A B C")

if __name__ == "__main__":
    unittest.main()
