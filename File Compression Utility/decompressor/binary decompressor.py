import json
import os
from utils.huffman import HuffmanNode, decode_data
from utils.logger import logger
from utils.exceptions import CompressionError

def rebuild_tree_from_codes(codes: dict) -> HuffmanNode:
    root = HuffmanNode()
    for char, code in codes.items():
        current = root
        for bit in code:
            if bit == '0':
                if current.left is None:
                    current.left = HuffmanNode()
                current = current.left
            else:
                if current.right is None:
                    current.right = HuffmanNode()
                current = current.right
        current.char = char
    return root

def decompress_binary_file(bin_path: str, code_path: str, output_path: str):
    try:
        logger.info("Starting binary decompression")

        if not os.path.exists(bin_path):
            raise FileNotFoundError(f"Binary file not found: {bin_path}")
        if not os.path.exists(code_path):
            raise FileNotFoundError(f"Code file not found: {code_path}")

        with open(code_path, 'r', encoding='utf-8') as f:
            codes = json.load(f)

        root = rebuild_tree_from_codes(codes)

        with open(bin_path, 'rb') as f:
            bit_data = ""
            byte = f.read(1)
            while byte:
                bits = bin(ord(byte))[2:].rjust(8, '0')
                bit_data += bits
                byte = f.read(1)

        padding = int(bit_data[:8], 2)
        encoded_data = bit_data[8:-padding]

        decoded_chars = decode_data(encoded_data, root)
        byte_data = bytes([ord(c) for c in decoded_chars])

        with open(output_path, 'wb') as f:
            f.write(byte_data)

        logger.info(f"Binary file decompressed → {output_path}")

    except FileNotFoundError as e:
        logger.error(str(e))
        raise CompressionError(str(e))
    except Exception as e:
        logger.exception("error during binary decompression")
        raise CompressionError(str(e))
