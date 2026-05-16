import os
import json
from utils.huffman import (
    HuffmanNode,
    decode_data
)
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


def decompress_archive(bin_path: str, meta_path: str, output_dir: str):
    try:
        if not os.path.exists(bin_path):
            raise FileNotFoundError(f"Binary archive not found: {bin_path}")
        if not os.path.exists(meta_path):
            raise FileNotFoundError(f"Metadata file not found: {meta_path}")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # We Will Load metadata
        with open(meta_path, 'r', encoding='utf-8') as f:
            meta = json.load(f)

        file_info = meta["file_info"]
        codes = meta["codes"]

        root = rebuild_tree_from_codes(codes)

        with open(bin_path, 'rb') as f:
            bit_data = ""
            byte = f.read(1)
            while byte:
                bits = bin(ord(byte))[2:].rjust(8, '0')
                bit_data += bits
                byte = f.read(1)

        padding = int(bit_data[:8], 2)
        encoded_data = bit_data[8:]
        encoded_data = encoded_data[:-padding]

        # Decode all data
        decoded_chars = decode_data(encoded_data, root)
        full_bytes = [ord(c) for c in decoded_chars]

        # Split and save files
        pointer = 0
        for file_path, length in file_info.items():
            filename = os.path.basename(file_path)
            output_path = os.path.join(output_dir, filename)

            with open(output_path, 'wb') as f:
                f.write(bytes(full_bytes[pointer:pointer + length]))
            pointer += length

            logger.info(f"Restored → {output_path}")

    except Exception as e:
        logger.exception("Error during archive decompression")
        raise CompressionError(f"Decompression failed: {str(e)}")
