import sys
import os
import argparse
from PyQt5.QtWidgets import QApplication

# GUI 
from GUI.my_app import CompressionApp

from compressor.text_compressor import compress_text_file
from decompressor.text_decompressor import decompress_text_file
from utils.stats import calculate_compression_ratio


def run_gui():
    app = QApplication(sys.argv)
    try:
        import qdarkstyle
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    except ImportError:
        pass

    window = CompressionApp()
    window.show()
    sys.exit(app.exec_())


def run_cli():
    print("Huffman File Compression Utility (CLI Mode)")
    print("1. Compress a text file")
    print("2. Decompress a file")
    choice = input("Enter choice (1 or 2): ").strip()

    if choice == '1':
        input_path = input("Enter path to input text file: ").strip()
        output_base = input("Enter base name for output files (without extension): ").strip()
        compress_text_file(input_path, output_base)
        ratio = calculate_compression_ratio(input_path, output_base + ".bin")
        print(f"Compression completed. Compression ratio: {ratio}:1")

    elif choice == '2':
        bin_path = input("Enter path to compressed .bin file: ").strip()
        code_path = input("Enter path to Huffman code .json file: ").strip()
        output_path = input("Enter path for output text file: ").strip()
        decompress_text_file(bin_path, code_path, output_path)
        print(f"Decompression completed. Output saved to: {output_path}")

    else:
        print("Invalid choice.")


def main():
    parser = argparse.ArgumentParser(description="Huffman Compression Utility")
    parser.add_argument('--cli', action='store_true', help="Run in command-line mode")
    args = parser.parse_args()

    if args.cli:
        run_cli()
    else:
        run_gui()


if __name__ == "__main__":
    main()
