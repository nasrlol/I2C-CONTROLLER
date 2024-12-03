from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtCore import Qt
import hardware_driver as lcd
import features as fe
import sys

F = fe.feat()  
L = lcd.LCD()  


class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("I2C CONTROLLER")
        self.setGeometry(200, 100, 800, 300)
        self.mainUI()

    def mainUI(self):
        central_widget = QWidget(self) 
        self.setCentralWidget(central_widget)

        self.label = QLabel("CONNECTED TO I2C DEVICE", self)
        self.label.setAlignment(Qt.AlignCenter)

        self.button = QPushButton("Clear Screen", self)
        self.button.clicked.connect(self.clear_screen)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)

        central_widget.setLayout(layout)

    def clear_screen(self):  
        F.clear()  
        self.label.setText("Cleared the LCD screen")  


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = mainWindow()
    window.show()
    sys.exit(app.exec())
