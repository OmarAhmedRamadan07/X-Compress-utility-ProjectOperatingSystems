import os 
import json
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

def compress_text_file(input_path: str, output_path: str):
    try:
        
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"File not found: {input_path}")

        with open(input_path, 'r', encoding='utf-8') as file:
            text = file.read()

        if not text.strip():
            raise CompressionError("Input text file is empty.")

        logger.info(f"Reading file: {input_path}")

        freq_map = build_frequency_map(text)
        root = build_huffman_tree(freq_map)
        codes = generate_huffman_codes(root)

        visualize_huffman_tree(root, output_path="archive/text_huffman_tree.png")
        logger.info("Huffman tree saved to archive/text_huffman_tree.png")

        encoded_data = encode_data(text, codes)

        padding = 8 - len(encoded_data) % 8
        encoded_data += '0' * padding
        padded_info = "{0:08b}".format(padding)
        encoded_data = padded_info + encoded_data

        b = bytearray()
        for i in range(0, len(encoded_data), 8):
            byte = encoded_data[i:i+8]
            b.append(int(byte, 2))

        bin_file_path = output_path + '.bin'
        with open(bin_file_path, 'wb') as binary_out:
            binary_out.write(bytes(b))

        with open(output_path + '_codes.json', 'w', encoding='utf-8') as json_out:
            json.dump(codes, json_out, ensure_ascii=False, indent=2)

        ratio = calculate_compression_ratio(input_path, bin_file_path)
        logger.info(f"Compression ratio: {ratio}:1")

        logger.info(f"Compressed: {input_path} → {output_path}.bin")
        logger.info(f"Saved Huffman codes → {output_path}_codes.json")

    except FileNotFoundError as e:
        logger.error(str(e))
        raise CompressionError(str(e))

    except CompressionError as e:
        logger.warning(str(e))
        raise

    except Exception as e:
        logger.exception("error during compression")
        raise CompressionError(f"error: {str(e)}")
