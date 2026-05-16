# utils/stats.py
import os
from utils.logger import logger

def calculate_compression_ratio(original_path: str, compressed_path: str) -> float:
    """Calculates the compression ratio."""
    try:
        original_size = os.path.getsize(original_path)
        compressed_size = os.path.getsize(compressed_path)
        
        if compressed_size == 0:
            return float('inf') # Infinite compression if compressed file is empty
        
        ratio = round(original_size / compressed_size, 2)
        return ratio
    except FileNotFoundError as e:
        logger.error(f"Error calculating ratio: {e}")
        return 0.0
    except Exception as e:
        logger.error(f"Error calculating ratio: {e}")
        return 0.0