import sys
import PySide6 import QtCore, QtWidgets, QtGui
from ui_form import Ui_GUI  # Assuming this is the file generated from your .ui file
# from hardware_driver import custom_greeting, pomodoro, system_readings, display_uptime, recognize_speech, save_notes


class gui(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_GUI()  # Assuming this is the auto-generated UI class
        self.ui.setupUi(self)
        self.setWindowTitle("LCD1602")





if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = gui()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
