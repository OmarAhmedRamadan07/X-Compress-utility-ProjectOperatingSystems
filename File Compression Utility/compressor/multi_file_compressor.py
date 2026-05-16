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

def compress_multiple_files(file_paths: list, output_archive_path: str):
    try:
        archive = {}
        all_data = ""
        total_original_size = 0  

        logger.info("Starting multi-file compression...")

        for file_path in file_paths:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")

            with open(file_path, 'rb') as f:
                content = f.read()

                if not content:
                    logger.warning(f"Skipped empty file: {file_path}")
                    continue

                all_data += ''.join([chr(byte) for byte in content])
                archive[file_path] = len(content)
                total_original_size += len(content)  

                logger.info(f"Read file: {file_path} ({len(content)} bytes)")

        if not all_data:
            raise CompressionError("All input files were empty. No data to compress.")

        freq_map = build_frequency_map(all_data)
        root = build_huffman_tree(freq_map)
        codes = generate_huffman_codes(root)

        visualize_huffman_tree(root, output_path="archive/multi_file_huffman_tree.png")
        logger.info("Huffman tree saved to archive/multi_file_huffman_tree.png")

        encoded_data = encode_data(all_data, codes)

        padding = 8 - len(encoded_data) % 8
        encoded_data += '0' * padding
        padded_info = f"{padding:08b}"
        encoded_data = padded_info + encoded_data

        byte_array = bytearray()
        for i in range(0, len(encoded_data), 8):
            byte_array.append(int(encoded_data[i:i+8], 2))

        bin_path = output_archive_path + '.bin'
        with open(bin_path, 'wb') as f:
            f.write(byte_array)

        logger.info(f"Archive created → {bin_path}")

        metadata = {
            "file_info": archive,
            "codes": codes
        }

        with open(output_archive_path + '_meta.json', 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        logger.info(f"Metadata saved → {output_archive_path}_meta.json")

        compressed_size = os.path.getsize(bin_path)
        if total_original_size > 0:
            ratio = round(total_original_size / compressed_size, 2)
            logger.info(f"Compression ratio: {ratio}:1")
        else:
            logger.warning("Cannot calculate compression ratio (original size = 0)")

    except FileNotFoundError as e:
        logger.error(str(e))
        raise CompressionError(str(e))

    except CompressionError as e:
        logger.warning(str(e))
        raise

    except Exception as e:
        logger.exception("error during multi-file compression")
        raise CompressionError(str(e))
