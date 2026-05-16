import json
import os
from utils.huffman import (
    build_frequency_map,
    build_huffman_tree,
    generate_huffman_codes,
    encode_data
)
from utils.logger import logger
from utils.exceptions import CompressionError
from utils.visualizer import visualize_huffman_tree
from utils.stats import calculate_compression_ratio  

def compress_binary_file(input_path: str, output_path: str):
    try:
        # Read binary data
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"File not found: {input_path}")

        with open(input_path, 'rb') as f:
            binary_data = f.read()

        if not binary_data:
            raise CompressionError("Binary file is empty.")

        logger.info(f"Reading binary file: {input_path}")

        # Convert bytes to pseudo text
        data_as_str = ''.join([chr(byte) for byte in binary_data])

        # Huffman components
        freq_map = build_frequency_map(data_as_str)
        root = build_huffman_tree(freq_map)
        codes = generate_huffman_codes(root)

        # Visualize Huffman Tree
        visualize_huffman_tree(root, output_path="archive/binary_huffman_tree.png")
        logger.info("Huffman tree saved to archive/binary_huffman_tree.png")

        encoded_data = encode_data(data_as_str, codes)

        padding = 8 - len(encoded_data) % 8
        encoded_data += '0' * padding
        padded_info = f"{padding:08b}"
        encoded_data = padded_info + encoded_data

        byte_array = bytearray()
        for i in range(0, len(encoded_data), 8):
            byte_array.append(int(encoded_data[i:i+8], 2))

        bin_file_path = output_path + '.bin'
        with open(bin_file_path, 'wb') as bin_file:
            bin_file.write(byte_array)

        with open(output_path + '_codes.json', 'w', encoding='utf-8') as json_file:
            json.dump(codes, json_file, ensure_ascii=False, indent=2)

        ratio = calculate_compression_ratio(input_path, bin_file_path)
        logger.info(f"Compression ratio: {ratio}:1")

        logger.info(f"Binary file compressed → {output_path}.bin")
        logger.info(f"Huffman codes saved → {output_path}_codes.json")

    except FileNotFoundError as e:
        logger.error(str(e))
        raise CompressionError(str(e))

    except CompressionError as e:
        logger.warning(str(e))
        raise

    except Exception as e:
        logger.exception("Unexpected error during binary compression")
        raise CompressionError(str(e))
