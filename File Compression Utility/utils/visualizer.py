import matplotlib.pyplot as plt
import matplotlib.patches as patches
from utils.huffman import HuffmanNode

def visualize_huffman_tree(root: HuffmanNode, output_path="archive/huffman_tree.png"):
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.axis('off')

    def get_tree_height(node):
        if node is None:
            return 0
        return 1 + max(get_tree_height(node.left), get_tree_height(node.right))

    def draw_node(node, x, y, dx, level):
        if node is None:
            return

        label = f"'{node.char}'\n{node.freq}" if node.char is not None else f"{node.freq}"
        ax.text(x, y, label, ha='center', va='center',
                bbox=dict(boxstyle="round", facecolor="lightblue", edgecolor="black"))

        if node.left:
            x_left = x - dx / (2 ** level)
            y_child = y - 1
            ax.plot([x, x_left], [y, y_child], 'k-')
            draw_node(node.left, x_left, y_child, dx, level + 1)

        if node.right:
            x_right = x + dx / (2 ** level)
            y_child = y - 1
            ax.plot([x, x_right], [y, y_child], 'k-')
            draw_node(node.right, x_right, y_child, dx, level + 1)

    tree_height = get_tree_height(root)
    draw_node(root, x=0, y=tree_height, dx=20, level=1)

    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f"Huffman tree saved as {output_path}")
