from text_compressor import compress_text_file
from text_decompressor import decompress_text_file
from binary_compressor import compress_binary_file
from binary_decompressor import decompress_binary_file
from multi_file_compressor import compress_multiple_files
from multi_file_decompressor import decompress_archive
from utils.logger import logger
from utils.exceptions import CompressionError

# --- Text Compression/Decompression Example ---
logger.info("--- Starting Text Compression Example ---")
INPUT_TEXT = "sample_text.txt"
OUTPUT_TEXT = "compressed_text"
DECOMPRESSED_TEXT = "restored_text.txt"

try:
    compress_text_file(INPUT_TEXT, OUTPUT_TEXT)
    decompress_text_file(f"{OUTPUT_TEXT}.bin", f"{OUTPUT_TEXT}_codes.json", DECOMPRESSED_TEXT)
    logger.info(f"Text compression/decompression successful. Result in {DECOMPRESSED_TEXT}")
except CompressionError as e:
    logger.error(f"Text compression failed: {e}")

# --- Multi-File Compression/Decompression Example ---
logger.info("\n--- Starting Multi-File Compression Example ---")
# Create a second dummy file for multi-file compression
with open("sample_binary.bin", 'wb') as f:
    f.write(bytes([65, 65, 66, 67, 65, 67])) # "AABCA" in binary
    
FILE_LIST = [INPUT_TEXT, "sample_binary.bin"]
OUTPUT_ARCHIVE = "multi_archive"
OUTPUT_DIR = "decompressed_files"

try:
    compress_multiple_files(FILE_LIST, OUTPUT_ARCHIVE)
    decompress_archive(f"{OUTPUT_ARCHIVE}.bin", f"{OUTPUT_ARCHIVE}_meta.json", OUTPUT_DIR)
    logger.info(f"Multi-file compression/decompression successful. Files restored in {OUTPUT_DIR}")
except CompressionError as e:
    logger.error(f"Multi-file compression failed: {e}")