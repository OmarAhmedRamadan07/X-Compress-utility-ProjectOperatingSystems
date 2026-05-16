import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog,
    QLabel, QRadioButton, QHBoxLayout, QTextEdit, QMessageBox,
    QLineEdit, QGroupBox, QComboBox, QSplitter, QProgressBar,
    QFrame, QGridLayout, QSizePolicy
)
from PyQt5.QtGui import QFont, QPixmap, QColor, QPalette, QPainter, QPen, QBrush, QLinearGradient
from PyQt5.QtCore import Qt, QTimer, QRectF

# Ensure these imports match your folder structure
from compressor.text_compressor import compress_text_file
from compressor.binary_compressor import compress_binary_file
from compressor.multi_file_compressor import compress_multiple_files
from decompressor.text_decompressor import decompress_text_file
from decompressor.archive_decompressor import decompress_archive
from utils.stats import calculate_compression_ratio

# --- Custom Circular Progress Bar Class ---
class CircularProgress(QWidget):
    def __init__(self):
        super().__init__()
        self.value = 0
        self.setMinimumSize(150, 150)
        
    def setValue(self, val):
        self.value = val
        self.repaint()

    def paintEvent(self, event):
        width = self.width()
        height = self.height()
        margin = 10
        radius = min(width, height) / 2 - margin
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Center point
        center = self.rect().center()
        
        # 1. Background Circle (Dark Purple/Grey)
        painter.setPen(QPen(QColor("#2d2d44"), 10, Qt.SolidLine, Qt.RoundCap))
        painter.drawEllipse(center, radius, radius)
        
        # 2. Progress Arc (Purple Accent)
        pen = QPen(QColor("#a259ff"), 10, Qt.SolidLine, Qt.RoundCap)
        painter.setPen(pen)
        
        # Angle calculations: 360 degrees * (value / 100)
        # PyQt draws arcs in 1/16th of a degree. Start at 90 degrees (Top)
        angle = int(-360 * (self.value / 100) * 16)
        start_angle = 90 * 16
        
        rect = QRectF(center.x() - radius, center.y() - radius, radius * 2, radius * 2)
        painter.drawArc(rect, start_angle, angle)
        
        # 3. Text in center
        painter.setPen(QColor("#ffffff"))
        painter.setFont(QFont("Segoe UI", 20, QFont.Bold))
        painter.drawText(self.rect(), Qt.AlignCenter, f"{self.value}%")

# --- Compression Ratio Visualizer Class ---
class RatioVisualizer(QWidget):
    def __init__(self):
        super().__init__()
        self._value = 0
        self._target_value = 0
        self._ratio_text = ""
        self.view_mode = "Ring"
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.setMinimumHeight(160)
        self.setMaximumHeight(200)

    def set_ratio(self, original_size, compressed_size):
        if original_size == 0:
            ratio = 0.0
            percent = 0
        else:
            ratio = original_size / compressed_size if compressed_size > 0 else 0.0
            percent = min(100, int((1 - compressed_size / original_size) * 100))

        self._target_value = percent
        self._ratio_text = f"{ratio:.2f}:1"
        self._value = 0
        self.timer.start(10)

    def animate(self):
        if self._value < self._target_value:
            self._value += 1
            self.update()
        else:
            self.timer.stop()

    def switch_view(self):
        self.view_mode = "Bar" if self.view_mode == "Ring" else "Ring"
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        if self.view_mode == "Ring":
            self._draw_ring(painter)
        else:
            self._draw_bar(painter)

    def _draw_ring(self, painter):
        rect = self.rect()
        radius = min(rect.width(), rect.height()) // 2 - 20
        center = rect.center()
        base_rect = QRectF(center.x() - radius, center.y() - radius, 2 * radius, 2 * radius)

        # Background Ring (Dark Purple)
        pen = QPen(QColor("#2d2d44"), 12, Qt.SolidLine, Qt.RoundCap)
        painter.setPen(pen)
        painter.drawArc(base_rect, 0, 360 * 16)

        # Foreground Ring (Cyan Blue)
        pen.setColor(QColor("#00d4ff")) 
        painter.setPen(pen)
        painter.drawArc(base_rect, 90 * 16, int(-self._value * 3.6 * 16))

        painter.setPen(QColor("#00d4ff"))
        font = QFont("Segoe UI", 14, QFont.Bold)
        painter.setFont(font)
        painter.drawText(rect, Qt.AlignCenter, f"{self._value}%\nSaved")

    def _draw_bar(self, painter):
        rect = self.rect()
        margin = 30
        bar_height = 30
        bar_width = rect.width() - 2 * margin
        bar_x = margin
        bar_y = rect.center().y() - bar_height // 2

        painter.setBrush(QColor("#2d2d44"))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(bar_x, bar_y, bar_width, bar_height, 15, 15)

        painter.setBrush(QColor("#00d4ff"))
        fill_width = int(bar_width * self._value / 100)
        painter.drawRoundedRect(bar_x, bar_y, fill_width, bar_height, 15, 15)

        painter.setPen(QColor("#00d4ff"))
        font = QFont("Segoe UI", 12, QFont.Bold)
        painter.setFont(font)
        painter.drawText(rect, Qt.AlignCenter, f"{self._value}% ({self._ratio_text})")


# --- Main Application Class ---
class CompressionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("X-->Compress")
        self.setGeometry(100, 100, 1100, 700)
        self.selected_files = []
        self.init_ui()
        self.apply_brand_style()

    def init_ui(self):
        # Main Container Layout (Horizontal Split)
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- LEFT SIDEBAR (Controls) ---
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(30, 40, 30, 40)
        sidebar_layout.setSpacing(25)

        # --- LOGO SECTION ---
        logo = QLabel()
        # Using raw string (r"...") for Windows path
        icon_path = r"C:\Users\hp\Downloads\File Compression Utility\icon.png"
        
        pixmap = QPixmap(icon_path)
        
        if not pixmap.isNull():
            # Scale to height 80px, keep aspect ratio, smooth edges
            logo.setPixmap(pixmap.scaledToHeight(80, Qt.SmoothTransformation))
        else:
            # Fallback if image not found
            logo.setText("CLOZR")
            logo.setFont(QFont("Segoe UI", 28, QFont.Bold))
            logo.setStyleSheet("color: white;")
            
        logo.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(logo)
        # --------------------

        sidebar_layout.addSpacing(20)

        # Mode Selection
        mode_label = QLabel("MODE")
        mode_label.setObjectName("SectionLabel")
        sidebar_layout.addWidget(mode_label)

        self.compress_radio = QRadioButton("Compress")
        self.decompress_radio = QRadioButton("Decompress")
        self.compress_radio.setChecked(True)
        
        mode_layout = QHBoxLayout()
        mode_layout.addWidget(self.compress_radio)
        mode_layout.addWidget(self.decompress_radio)
        sidebar_layout.addLayout(mode_layout)

        # File Type
        type_label = QLabel("TYPE")
        type_label.setObjectName("SectionLabel")
        sidebar_layout.addWidget(type_label)
        
        self.file_type_box = QComboBox()
        self.file_type_box.addItems(["Text File", "Binary File", "Multiple Files"])
        sidebar_layout.addWidget(self.file_type_box)

        # File Selection
        self.file_button = QPushButton("Select Files")
        self.file_button.setCursor(Qt.PointingHandCursor)
        self.file_button.clicked.connect(self.select_file)
        sidebar_layout.addWidget(self.file_button)
        
        self.file_label = QLabel("No files selected")
        self.file_label.setStyleSheet("color: #7d7d99; font-size: 11px;")
        self.file_label.setWordWrap(True)
        sidebar_layout.addWidget(self.file_label)

        # Output Path
        out_label = QLabel("OUTPUT")
        out_label.setObjectName("SectionLabel")
        sidebar_layout.addWidget(out_label)

        output_container = QHBoxLayout()
        self.output_path = QLineEdit()
        self.output_path.setPlaceholderText("Output directory...")
        self.output_button = QPushButton("...")
        self.output_button.setFixedWidth(40)
        self.output_button.clicked.connect(self.select_output_path)
        output_container.addWidget(self.output_path)
        output_container.addWidget(self.output_button)
        sidebar_layout.addLayout(output_container)

        sidebar_layout.addStretch()

        # Run Button
        self.run_button = QPushButton("START PROCESS")
        self.run_button.setObjectName("RunButton")
        self.run_button.setCursor(Qt.PointingHandCursor)
        self.run_button.clicked.connect(self.run_action)
        self.run_button.setMinimumHeight(50)
        sidebar_layout.addWidget(self.run_button)

        # --- RIGHT CONTENT AREA ---
        content_area = QFrame()
        content_area.setObjectName("ContentArea")
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(40, 40, 40, 40)
        content_layout.setSpacing(20)

        # Top Visualization Row
        viz_layout = QHBoxLayout()
        
        # 1. Circular Progress (Custom Widget)
        prog_container = QVBoxLayout()
        prog_label = QLabel("PROGRESS")
        prog_label.setStyleSheet("color: #a259ff; font-weight: bold;")
        prog_label.setAlignment(Qt.AlignCenter)
        
        self.progress_bar = CircularProgress() # Custom Circle Bar
        
        prog_container.addWidget(prog_label)
        prog_container.addWidget(self.progress_bar, alignment=Qt.AlignCenter)
        viz_layout.addLayout(prog_container, 1)

        # 2. Ratio Viz
        ratio_container = QVBoxLayout()
        ratio_label = QLabel("EFFICIENCY")
        ratio_label.setStyleSheet("color: #00d4ff; font-weight: bold;")
        ratio_label.setAlignment(Qt.AlignCenter)

        self.ratio_visualizer = RatioVisualizer()
        self.toggle_chart_btn = QPushButton("Toggle View")
        self.toggle_chart_btn.setObjectName("GhostButton")
        self.toggle_chart_btn.clicked.connect(self.ratio_visualizer.switch_view)
        
        ratio_container.addWidget(ratio_label)
        ratio_container.addWidget(self.ratio_visualizer)
        ratio_container.addWidget(self.toggle_chart_btn)
        viz_layout.addLayout(ratio_container, 1)

        content_layout.addLayout(viz_layout)

        # Divider
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("background-color: #2d2d44; border: none; height: 1px;")
        content_layout.addWidget(line)

        # Bottom Area: Logs and Tree View Splitter
        splitter = QSplitter(Qt.Horizontal)
        splitter.setHandleWidth(2)
        
        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        self.log_box.setPlaceholderText("System logs will appear here...")
        splitter.addWidget(self.log_box)

        self.tree_view = QLabel("Visual Tree Data")
        self.tree_view.setAlignment(Qt.AlignCenter)
        self.tree_view.setStyleSheet("background-color: #1a1a2e; border: 2px dashed #2d2d44; color: #555; border-radius: 10px;")
        splitter.addWidget(self.tree_view)
        
        # Set splitter sizes
        splitter.setSizes([300, 400])
        content_layout.addWidget(splitter)

        # Final Assembly
        main_layout.addWidget(sidebar, 3) 
        main_layout.addWidget(content_area, 7) 
        self.setLayout(main_layout)

    def apply_brand_style(self):
        # Global Palette setup (Deep Blue/Purple theme)
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#13131f")) # Very dark blue bg
        palette.setColor(QPalette.WindowText, QColor("#ffffff"))
        self.setPalette(palette)

        self.setFont(QFont("Segoe UI", 10))

        # Modern CSS Styling
        self.setStyleSheet("""
            QWidget {
                background-color: #13131f;
                color: #ffffff;
            }
            
            QFrame#Sidebar {
                background-color: #1a1a2e;
                border-right: 1px solid #2d2d44;
            }
            
            QFrame#ContentArea {
                background-color: #13131f;
            }

            QLabel#SectionLabel {
                color: #a259ff;
                font-weight: bold;
                font-size: 12px;
                margin-top: 10px;
            }

            /* Toggle/Radio Styling */
            QRadioButton {
                background-color: #2d2d44;
                padding: 8px 15px;
                border-radius: 5px;
                color: #aaa;
            }
            QRadioButton::indicator {
                width: 0px; 
                height: 0px; 
            }
            QRadioButton:checked {
                background-color: #a259ff;
                color: white;
                font-weight: bold;
            }

            /* Combo Box */
            QComboBox {
                background-color: #2d2d44;
                border: 1px solid #3d3d5c;
                border-radius: 5px;
                padding: 8px;
                color: white;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: #2d2d44;
                selection-background-color: #a259ff;
                color: white;
            }

            /* Inputs */
            QLineEdit {
                background-color: #2d2d44;
                border: 1px solid #3d3d5c;
                border-radius: 5px;
                padding: 8px;
                color: white;
            }

            /* Standard Buttons */
            QPushButton {
                background-color: #2d2d44;
                border: 1px solid #a259ff;
                color: #a259ff;
                border-radius: 6px;
                padding: 8px 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2d2d44;
                border: 1px solid #ffffff;
                color: white;
            }

            /* Run Button (Primary) */
            QPushButton#RunButton {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #7F00FF, stop:1 #E100FF);
                color: white;
                border: none;
                font-size: 14px;
                border-radius: 8px;
            }
            QPushButton#RunButton:hover {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #8F10FF, stop:1 #F110FF);
            }

            /* Ghost Button */
            QPushButton#GhostButton {
                background-color: transparent;
                border: none;
                color: #666;
            }
            QPushButton#GhostButton:hover {
                color: #00d4ff;
            }

            /* Logs */
            QTextEdit {
                background-color: #0f0f18;
                border: 1px solid #2d2d44;
                border-radius: 8px;
                color: #00ff9d; /* Matrix green text for logs */
                font-family: Consolas, monospace;
                padding: 10px;
            }

            /* Splitter */
            QSplitter::handle {
                background-color: #2d2d44;
            }
        """)

    def auto_detect_file_type(self, filename):
        if filename.endswith('.txt'):
            return "Text File"
        elif filename.endswith('.bin'):
            return "Binary File"
        else:
            return "Multiple Files"

    def select_file(self):
        mode = "Compress" if self.compress_radio.isChecked() else "Decompress"
        if mode == "Compress":
            files, _ = QFileDialog.getOpenFileNames(self, "Select File(s) to Compress")
        else:
            files, _ = QFileDialog.getOpenFileNames(self, "Select Compressed File(s)")
        self.selected_files = files
        self.file_label.setText("\n".join([os.path.basename(f) for f in files]) if files else "No file(s) selected")
        if files:
            self.output_path.setText(os.path.splitext(files[0])[0] + "_output")
            ftype = self.auto_detect_file_type(files[0])
            idx = self.file_type_box.findText(ftype)
            if idx != -1:
                self.file_type_box.setCurrentIndex(idx)

    def select_output_path(self):
        path = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if path:
            if self.selected_files:
                base = os.path.splitext(os.path.basename(self.selected_files[0]))[0]
                self.output_path.setText(os.path.join(path, base + "_output"))
            else:
                self.output_path.setText(path)

    def run_action(self):
        files = self.selected_files
        out_base = self.output_path.text().strip()
        mode = "Compress" if self.compress_radio.isChecked() else "Decompress"
        ftype = self.file_type_box.currentText()

        if not files or not all(os.path.exists(f) for f in files):
            QMessageBox.warning(self, "Error", "Please select valid file(s).")
            return
        if not out_base:
            QMessageBox.warning(self, "Error", "Please set an output path.")
            return

        try:
            self.log_box.clear()
            self.tree_view.clear()
            self.tree_view.setText("Processing...")
            self.progress_bar.setValue(0)
            self.ratio_visualizer.set_ratio(0, 1)

            if mode == "Compress":
                self.progress_bar.setValue(25)
                # Processing logic
                if ftype == "Text File":
                    compress_text_file(files[0], out_base)
                    tree = "archive/text_huffman_tree.png"
                elif ftype == "Binary File":
                    compress_binary_file(files[0], out_base)
                    tree = "archive/binary_huffman_tree.png"
                else:
                    compress_multiple_files(files, out_base)
                    tree = "archive/multi_file_huffman_tree.png"

                self.progress_bar.setValue(75)
                
                # Stats
                ratio = calculate_compression_ratio(files[0], out_base + ".bin")
                original = os.path.getsize(files[0])
                compressed = os.path.getsize(out_base + ".bin")

                self.log_box.append(">> COMPRESSION COMPLETE")
                self.log_box.append(f"Original:   {original} B")
                self.log_box.append(f"Compressed: {compressed} B")
                self.log_box.append(f"Ratio:      {ratio:.2f}:1")
                self.log_box.append("Tree visualization generated.")

                self.ratio_visualizer.set_ratio(original, compressed)

                if os.path.exists(tree):
                    self.tree_view.setPixmap(QPixmap(tree).scaledToWidth(380))
                    self.tree_view.setText("")

            else:
                self.progress_bar.setValue(25)
                if ftype == "Multiple Files":
                    decompress_archive(files[0], files[0].replace(".bin", "_meta.json"), os.path.dirname(out_base))
                else:
                    decompress_text_file(files[0], files[0].replace(".bin", "_codes.json"), out_base + "_decompressed.txt")
                self.log_box.append(">> DECOMPRESSION COMPLETE")
                self.tree_view.setText("Decompression Done")

            self.progress_bar.setValue(100)

        except Exception as e:
            self.progress_bar.setValue(0)
            self.log_box.append(f"ERROR: {str(e)}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CompressionApp()
    window.show()
    sys.exit(app.exec_())