import re
import random
import heapq
from graphviz import Digraph
import os

class Graph:
    def __init__(self):
        self.nodes = {}  # key: word, value: dict of neighbors and weights

    def add_edge(self, u, v):
        u = u.lower()
        v = v.lower()
        if u not in self.nodes:
            self.nodes[u] = {}
        if v not in self.nodes[u]:
            self.nodes[u][v] = 0
        self.nodes[u][v] += 1
        if v not in self.nodes:
            self.nodes[v] = {}

def build_graph(filename):
    graph = Graph()
    with open(filename, 'r') as file:
        text = file.read()
    text = re.sub(r'[^a-zA-Z]', ' ', text)
    words = [word.lower() for word in text.split()]
    for i in range(len(words) - 1):
        u = words[i]
        v = words[i+1]
        graph.add_edge(u, v)
    if words:
        last_word = words[-1]
        if last_word not in graph.nodes:
            graph.nodes[last_word] = {}
    return graph

graph = None

def showDirectedGraph():
    global graph
    dot = Digraph(comment='Directed Graph', format='png')
    for node in graph.nodes:
        dot.node(node)
    for u in graph.nodes:
        for v, weight in graph.nodes[u].items():
            dot.edge(u, v, label=str(weight))
    dot.render('graph.gv', view=True)  
    return "Graph saved as graph.gv.png"

def queryBridgeWords(word1, word2):
    global graph
    word1_lower = word1.lower()
    word2_lower = word2.lower()
    if word1_lower not in graph.nodes or word2_lower not in graph.nodes:
        if word1_lower not in graph.nodes and word2_lower not in graph.nodes:
            return f"No {word1} and {word2} in the graph!"
        elif word1_lower not in graph.nodes:
            return f"No {word1} in the graph!"
        else:
            return f"No {word2} in the graph!"
    bridge_words = []
    if word1_lower in graph.nodes:
        for word3 in graph.nodes[word1_lower]:
            if word2_lower in graph.nodes.get(word3, {}):
                bridge_words.append(word3)
    if not bridge_words:
        return f"No bridge words from {word1} to {word2}!"
    else:
        def format_list(items):
            if len(items) == 1:
                return items[0]
            elif len(items) == 2:
                return f"{items[0]} and {items[1]}"
            else:
                return ', '.join(items[:-1]) + f", and {items[-1]}"
        formatted = format_list(bridge_words)
        return f"The bridge words from {word1} to {word2} are: {formatted}."

def generateNewText(inputText):
    global graph
    words = inputText.split()
    new_words = []
    for i in range(len(words) - 1):
        wordA = words[i].lower()
        wordB = words[i+1].lower()
        bridge_words = []
        if wordA in graph.nodes:
            for word3 in graph.nodes[wordA]:
                if wordB in graph.nodes.get(word3, {}):
                    bridge_words.append(word3)
        if bridge_words:
            chosen = random.choice(bridge_words)
            new_words.append(words[i])
            new_words.append(chosen)
        else:
            new_words.append(words[i])
    new_words.append(words[-1])
    return ' '.join(new_words)

def calcShortestPath(word1, word2):
    global graph
    start = word1.lower()
    end = word2.lower()
    if start not in graph.nodes or end not in graph.nodes:
        return f"No path from {word1} to {word2}!"
    distances = {node: float('inf') for node in graph.nodes}
    distances[start] = 0
    predecessors = {}
    heap = [(0, start)]
    while heap:
        current_dist, current_node = heapq.heappop(heap)
        if current_node == end:
            break
        if current_dist > distances[current_node]:
            continue
        for neighbor, weight in graph.nodes[current_node].items():
            distance = current_dist + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = current_node
                heapq.heappush(heap, (distance, neighbor))
    if distances[end] == float('inf'):
        return f"No path from {word1} to {word2}!"
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = predecessors.get(current)
    path.reverse()
    path_str = '→'.join(path)
    return f"Shortest path: {path_str} with length {distances[end]}."

def calcPageRank(word):
    global graph
    d = 0.85
    max_iter = 100
    tol = 1e-6
    nodes = graph.nodes.keys()
    N = len(nodes)
    pr = {node: 1/N for node in nodes}
    for _ in range(max_iter):
        new_pr = {}
        for node in nodes:
            incoming_sum = 0.0
            for v in nodes:
                if node in graph.nodes[v]:
                    Lv = len(graph.nodes[v])
                    if Lv > 0:
                        incoming_sum += pr[v] / Lv
            new_pr[node] = (1 - d)/N + d * incoming_sum
        delta = sum(abs(new_pr[node] - pr[node]) for node in nodes)
        if delta < tol:
            break
        pr = new_pr
    return pr.get(word.lower(), 0.0)

def randomWalk():
    global graph
    nodes = list(graph.nodes.keys())
    if not nodes:
        return ""
    current = random.choice(nodes)
    path = [current]
    visited_edges = set()
    while True:
        if current not in graph.nodes or not graph.nodes[current]:
            break
        neighbors = list(graph.nodes[current].keys())
        next_node = random.choice(neighbors)
        edge = (current, next_node)
        if edge in visited_edges:
            break
        visited_edges.add(edge)
        path.append(next_node)
        current = next_node
    return ' '.join(path)

def main():
    global graph
    import sys
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = input("Enter the path to the text file: ")
    graph = build_graph(filename)
    while True:
        print("\nSelect a function:")
        print("1. Show directed graph")
        print("2. Query bridge words")
        print("3. Generate new text")
        print("4. Calculate shortest path")
        print("5. Calculate PageRank")
        print("6. Random walk")
        print("7. Exit")
        choice = input("Enter your choice (1-7): ")
        if choice == '1':
            showDirectedGraph()
        elif choice == '2':
            word1 = input("Enter word1: ")
            word2 = input("Enter word2: ")
            print(queryBridgeWords(word1, word2))
        elif choice == '3':
            text = input("Enter the new text: ")
            print("Generated text:", generateNewText(text))
        elif choice == '4':
            word1 = input("Enter word1: ")
            word2 = input("Enter word2: ")
            print(calcShortestPath(word1, word2))
        elif choice == '5':
            word = input("Enter the word: ")
            pr = calcPageRank(word)
            print(f"PageRank of {word}: {pr:.4f}")
        elif choice == '6':
            walk = randomWalk()
            print("Random walk:", walk)
            with open("random_walk.txt", 'w') as f:
                f.write(walk)
            print("Saved to random_walk.txt")
        elif choice == '7':
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()