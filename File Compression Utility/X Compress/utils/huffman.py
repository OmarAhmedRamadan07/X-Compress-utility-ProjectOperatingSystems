# utils/huffman.py

import heapq
from collections import Counter

class HuffmanNode:
    """Represents a node in the Huffman tree."""
    def __init__(self, char=None, freq=0, left=None, right=None):
        self.char = char  # Character (only set for leaf nodes)
        self.freq = freq  # Frequency (priority for the heap)
        self.left = left  # Left child node
        self.right = right # Right child node

    # Necessary for heapq comparison
    def __lt__(self, other):
        return self.freq < other.freq

    def __repr__(self):
        return f"Node(char='{self.char}', freq={self.freq})"

def build_frequency_map(data: str) -> dict:
    """Builds a frequency map from the input data."""
    return Counter(data)

def build_huffman_tree(freq_map: dict) -> HuffmanNode:
    """Builds the Huffman tree from the frequency map."""
    priority_queue = []
    # Create a list of leaf nodes (Node, frequency)
    for char, freq in freq_map.items():
        heapq.heappush(priority_queue, HuffmanNode(char, freq))

    # Build the tree
    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue)
        right = heapq.heappop(priority_queue)

        # Create a new internal node
        merged = HuffmanNode(freq=left.freq + right.freq, left=left, right=right)
        heapq.heappush(priority_queue, merged)

    return priority_queue[0]

def generate_huffman_codes(root: HuffmanNode, current_code: str = "", codes: dict = None) -> dict:
    """Generates the Huffman codes from the tree."""
    if codes is None:
        codes = {}

    if root.char is not None:
        # Leaf node reached, store the code
        codes[root.char] = current_code if current_code else '0' # Handles single character case
        return codes

    if root.left:
        generate_huffman_codes(root.left, current_code + "0", codes)
    if root.right:
        generate_huffman_codes(root.right, current_code + "1", codes)

    return codes

def encode_data(data: str, codes: dict) -> str:
    """Encodes the input data string using the Huffman codes."""
    encoded = "".join(codes[char] for char in data)
    return encoded

def decode_data(encoded_data: str, root: HuffmanNode) -> str:
    """Decodes the encoded bit string using the Huffman tree."""
    decoded_chars = []
    current_node = root

    for bit in encoded_data:
        if bit == '0':
            current_node = current_node.left
        else:
            current_node = current_node.right

        if current_node.char is not None:
            # Found a character (leaf node)
            decoded_chars.append(current_node.char)
            current_node = root # Reset to root for the next character

    return "".join(decoded_chars)