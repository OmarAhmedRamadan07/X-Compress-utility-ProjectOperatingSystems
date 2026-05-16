import heapq
from collections import defaultdict

class HuffmanNode:
    def __init__(self, char=None, freq=0):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


def build_frequency_map(data: str) -> dict:
    freq_map = defaultdict(int)
    for char in data:
        freq_map[char] += 1
    return dict(freq_map)


def build_huffman_tree(freq_map: dict) -> HuffmanNode:
    heap = []
    for char, freq in freq_map.items():
        node = HuffmanNode(char, freq)
        heapq.heappush(heap, node)

    while len(heap) > 1:
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)

        merged = HuffmanNode(None, node1.freq + node2.freq)
        merged.left = node1
        merged.right = node2

        heapq.heappush(heap, merged)

    return heap[0] if heap else None


def generate_huffman_codes(root: HuffmanNode) -> dict:
    codes = {}

    def traverse(node, current_code):
        if node is None:
            return
        if node.char is not None:
            codes[node.char] = current_code
            return
        traverse(node.left, current_code + "0")
        traverse(node.right, current_code + "1")

    traverse(root, "")
    return codes


def encode_data(data: str, codes: dict) -> str:
    encoded_output = ''
    for char in data:
        encoded_output += codes[char]
    return encoded_output


def decode_data(encoded_data: str, root: HuffmanNode) -> str:
    decoded_output = ''
    current_node = root

    for bit in encoded_data:
        if bit == '0':
            current_node = current_node.left
        else:
            current_node = current_node.right

        if current_node.char is not None:
            decoded_output += current_node.char
            current_node = root

    return decoded_output

