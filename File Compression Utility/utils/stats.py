import os

def calculate_compression_ratio(original_path: str, compressed_path: str) -> float:
    try:
        original_size = os.path.getsize(original_path)
        compressed_size = os.path.getsize(compressed_path)

        if compressed_size == 0:
            return float('inf')  

        ratio = original_size / compressed_size
        return round(ratio, 2)

    except Exception as e:
        print(f"Error calculating compression ratio: {e}")
        return 0.0
