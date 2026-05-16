# Clozr File Compressor (X-Compress) 🗜️

A comprehensive Python-based utility for efficient file compression and decompression using **Huffman Coding**. The application features a professional Graphical User Interface (GUI) built with PyQt5, alongside a fully functional Command-Line Interface (CLI) for server environments and automation.

Developed as a core Operating Systems project at **El Sewedy University of Technology (SUT)**.

---

## 🚀 Key Features

* **Lossless Data Compression:** Guarantees perfect reconstruction of the original files with zero data loss.
* **Format Flexibility:** Supports the compression of text files (.txt), binary files (.bin), and multi-file archives.
* **Dual Interface Modes:**
  * **GUI Mode:** An intuitive, dark-themed interface (#1C2B39) with interactive compression ratio displays (Ring/Bar charts) and operation logs.
  * **CLI Mode:** Command-line operations for advanced users (python main.py --cli).
* **Huffman Tree Visualization:** Generates and displays a visual representation of the Huffman tree post-compression.
* **Robust Error Handling:** Safely manages empty files, missing paths, and runtime errors.

---

## 🏗️ System Architecture & Modules

The software is built with a clean, modular architecture to ensure maintainability and high performance:

* **compressor.py**: The encoding engine. Calculates character frequencies, builds the Huffman tree, generates binary codes, and outputs the compressed .bin files along with .json metadata/keys.
* **decompressor.py**: The extraction engine. Reconstructs the original files exactly using the saved Huffman dictionary.
* **gui.py**: The frontend layer utilizing PyQt5.QtWidgets for a responsive and professional user experience.
* **utils.py**: Helper functions including the Logger, compression ratio calculators, and tree visualization tools.

---

## ⚙️ How the Algorithm Works

1. **Frequency Analysis:** Scans the input data to count byte/character occurrences.
2. **Tree Construction:** Builds a binary Huffman tree, assigning shorter binary codes to highly frequent symbols and longer codes to rare ones.
3. **Encoding:** Translates the original data into a compact binary string based on the generated prefix codes.
4. **Storage:** Saves the compressed binary data along with a .json file containing the Huffman dictionary needed for future restoration.

---

## 🛠️ Requirements & Installation

**Prerequisites:**
* Python 3.10 or higher
* OS: Windows / Linux / MacOS

**Dependencies:**
pip install PyQt5
pip install qdarkstyle

**Run the Application:**
* **GUI Mode:** python main.py
* **CLI Mode:** python main.py --cli

---

## 📸 Screenshots

![Clozr GUI](image_4582de.png)

---

## 👥 Development Team

This project was developed collaboratively by:
* **Omar Ahmed Ramadan**
* **Youssef Amr**
* **Mohamed Nasser**
* **Ahmed Mohamed**
* **Omar**
