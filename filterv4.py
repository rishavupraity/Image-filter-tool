
'''
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout,
    QWidget, QHBoxLayout, QSizePolicy
)
from PySide6.QtGui import QPixmap, QKeyEvent
from PySide6.QtCore import Qt

'''

import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout,
    QWidget, QHBoxLayout, QSizePolicy, QMenu, QMessageBox, QSystemTrayIcon
)
from PySide6.QtGui import QPixmap, QKeyEvent, QIcon, QAction  # Correct import for QIcon and QAction
from PySide6.QtCore import Qt


class ImageFilterTool(QMainWindow):
    def __init__(self, image_dir):
        super().__init__()
        self.setWindowTitle("Image Filter Tool")

        # Initialize variables
        self.image_dir = image_dir
        self.image_list = [f for f in os.listdir(image_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]

        self.image_count = len(self.image_list)
        #print(self.image_count)


        # Sort images by filename (alphabetical order)
        self.image_list = sorted(self.image_list)

        self.current_index = 0

        # Main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Set up UI components
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)

        self.filename_label = QLabel()
        self.filename_label.setAlignment(Qt.AlignCenter)
        self.filename_label.setStyleSheet("font-size: 14px; color: #fff;")

        # Buttons
        self.prev_button = QPushButton("< Previous")
        self.next_button = QPushButton("Next >")
        self.move_button = QPushButton("[ Move ]")

        # Set button sizes and styles
        button_style = "color: #000000; font-size: 14px; padding: 10px 20px;"

        self.prev_button.setStyleSheet(button_style + "background-color: #ADD8E6;")  # Light Blue
        self.move_button.setStyleSheet(button_style + "background-color: #F08080;")  # Light Red
        self.next_button.setStyleSheet(button_style + "background-color: #90EE90;")  # Light Green

        self.prev_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.move_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.next_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Connect buttons to their respective functions
        self.prev_button.clicked.connect(self.show_previous_image)
        self.next_button.clicked.connect(self.show_next_image)
        self.move_button.clicked.connect(self.move_current_image)

        # Layout setup
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.prev_button)
        button_layout.addWidget(self.move_button)
        button_layout.addWidget(self.next_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.image_label)
        main_layout.addWidget(self.filename_label)
        main_layout.addLayout(button_layout)

        self.central_widget.setLayout(main_layout)

        # Display the first image
        if self.image_list:
            self.display_image()
        else:
            self.image_label.setText("No images found in the directory.")


        self.setFocusPolicy(Qt.StrongFocus)


        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Image Information")
        msg.setText(f"There is {self.image_count} files found.\n  Press OK to continue filtering")
        msg.exec()


    def display_image(self):
        """Displays the current image in its original size and adjusts window size."""
        image_path = os.path.join(self.image_dir, self.image_list[self.current_index])
        pixmap = QPixmap(image_path)

        if pixmap.isNull():
            self.image_label.setText("Failed to load image.")
            self.filename_label.setText("")
        else:
            self.image_label.setPixmap(pixmap)
            self.resize(pixmap.width(), pixmap.height() + 100)
            self.filename_label.setText(os.path.basename(image_path))

    def show_next_image(self):
        """Show the next image in the directory."""
        if self.image_list:
            self.current_index = (self.current_index + 1) % len(self.image_list)
            self.display_image()
            self.move_button.setText("[ Move ]")

    def show_previous_image(self):
        """Show the previous image in the directory."""
        if self.image_list:
            self.current_index = (self.current_index - 1) % len(self.image_list)
            self.display_image()
            self.move_button.setText("[ Move ]")

    def move_current_image(self):
        """Move the current image name to a text file."""
        if self.image_list:
            image_name = self.image_list[self.current_index]
            with open('moved_images.txt', 'a') as file:
                file.write(f"{image_name}\n")

            print(f"Image '{image_name}' moved.")

            # Change the move button label to "Moved"
            self.move_button.setText("[ Moved ]")
            # Disable the button to prevent moving the same image again
            #self.move_button.setEnabled(False)



    def keyPressEvent(self, event: QKeyEvent):
        """Handle key press events for navigation."""
        if event.key() == Qt.Key_Left:
            self.show_previous_image()
            #print("Left key pressed")
        elif event.key() == Qt.Key_Right:
            self.show_next_image()
            #print("Right key pressed")
        elif event.key() == Qt.Key_Space:
            self.move_current_image()
            #print("SpaceBar key pressed")

def main():
    import sys
    app = QApplication(sys.argv)

    # Provide the path to your image directory
    image_dir = "/home/user/Downloads/Airplane_data/frame_filter/output_frames" #/home/user/Downloads/Airplane_data/frame_filter/output_frames
    viewer = ImageFilterTool(image_dir)
    viewer.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
