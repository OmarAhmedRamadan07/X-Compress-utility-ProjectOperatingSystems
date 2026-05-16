import logging
import os

# We Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

logger = logging.getLogger("FileCompressor")
logger.setLevel(logging.DEBUG)

# For File handl
file_handler = logging.FileHandler("logs/compression.log")
file_handler.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)
