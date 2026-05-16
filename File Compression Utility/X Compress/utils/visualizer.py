# utils/visualizer.py
import pydot
from utils.huffman import HuffmanNode
from utils.logger import logger

def visualize_huffman_tree(root: HuffmanNode, output_path: str):
    """Generates a visualization of the Huffman tree and saves it as an image."""
    
    graph = pydot.Dot(graph_type='graph', bgcolor='white')
    node_counter = 0

    def add_nodes_edges(node, parent_name=None, edge_label=''):
        nonlocal node_counter
        
        # Determine the label for the current node
        if node.char is not None:
            # Leaf node: label is 'Char (Freq)'
            label = f"'{node.char}'\\n({node.freq})"
        else:
            # Internal node: label is 'Freq'
            label = f"({node.freq})"

        # Create a unique name for the node in the graph
        node_name = f"node{node_counter}"
        node_counter += 1
        
        # Add the node to the graph
        pdot_node = pydot.Node(node_name, label=label, shape="circle")
        graph.add_node(pdot_node)

        if parent_name is not None:
            # Add an edge from the parent to the current node
            pdot_edge = pydot.Edge(parent_name, node_name, label=edge_label)
            graph.add_edge(pdot_edge)
            
        # Recurse for children
        if node.left:
            add_nodes_edges(node.left, node_name, '0')
        if node.right:
            add_nodes_edges(node.right, node_name, '1')

    # Start the visualization from the root
    if root:
        add_nodes_edges(root)

    # Save the graph to a file (e.g., PNG)
    try:
        graph.write_png(output_path)
    except Exception as e:
        logger.error(f"Failed to save Huffman tree visualization: {e}")
        logger.error("Make sure 'graphviz' is installed on your system.")