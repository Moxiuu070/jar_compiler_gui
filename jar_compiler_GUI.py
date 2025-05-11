import os
import subprocess
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QFileDialog, QWidget, QVBoxLayout, QLabel, QDialog, QDialogButtonBox
)
from PySide6.QtCore import Qt


class ViewerPopup(QDialog):
    def __init__(self, content, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Viewer")
        self.setGeometry(200, 200, 600, 400)
        layout = QVBoxLayout()
        self.text_area = QLabel(content)
        layout.addWidget(self.text_area)

        # Add a Close button
        buttons = QDialogButtonBox(QDialogButtonBox.Close)
        buttons.rejected.connect(self.accept)
        layout.addWidget(buttons)

        self.setLayout(layout)


class JarCompilerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("JAR Compiler GUI")
        self.setGeometry(100, 100, 600, 400)

        # Create the layout
        main_layout = QVBoxLayout()
        self.compile_button = QPushButton("Compile Folder to JAR")
        self.compile_button.clicked.connect(self.compile_folder_to_jar)

        # Add widgets to the layout
        self.debug_label = QLabel("Debug: Ready")
        self.output_label = QLabel("Output: No action yet")

        # Moxiu link
        self.moxiu_label = QLabel('<a href="https://github.com/Moxiuu070">Made by Moxiuu070</a>')
        self.moxiu_label.setOpenExternalLinks(True)

        main_layout.addWidget(self.compile_button)
        main_layout.addWidget(self.debug_label)
        main_layout.addWidget(self.output_label)
        main_layout.addWidget(self.moxiu_label)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def compile_folder_to_jar(self):
        # Select the folder to compile
        folder = QFileDialog.getExistingDirectory(self, "Select Folder to Compile")
        if not folder:
            return

        # Use current directory to create compiled folder
        current_dir = os.path.dirname(os.path.abspath(__file__))
        compiled_folder = os.path.join(current_dir, "compiled")
        os.makedirs(compiled_folder, exist_ok=True)

        # Set the output file path
        output_path = os.path.join(compiled_folder, "output.jar")

        # Update debug and output labels
        self.debug_label.setText("Debug: Compiling folder to JAR...")
        
        # Ensure jar.exe is in the bin directory
        jar_exe = os.path.join(current_dir, "bin", "jar.exe")
        if not os.path.exists(jar_exe):
            popup = ViewerPopup("Missing jar.exe in the 'bin' folder.")
            popup.exec()  # This will now work
            return

        # Compile the folder to a JAR using the specific jar.exe
        result = subprocess.run([jar_exe, "cf", output_path, "-C", folder, "."], capture_output=True, text=True)

        # Check the result of the compilation
        if result.returncode == 0:
            self.output_label.setText(f"Output: JAR compiled successfully: {output_path}")
            popup = ViewerPopup(f"JAR compiled successfully: {output_path}")
        else:
            self.output_label.setText(f"Output: Error compiling JAR")
            popup = ViewerPopup(f"Error compiling JAR:\n{result.stderr}")
        
        popup.exec()  # This will now work


if __name__ == "__main__":
    app = QApplication([])
    window = JarCompilerGUI()  # Use JarCompilerGUI for compiling JAR files
    window.show()
    app.exec()
