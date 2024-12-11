import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from Project1_UI import Ui_VotingMenu
from Project1_Logic import Logic

if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_VotingMenu()
    ui.setupUi(MainWindow)

    # Initialize the Logic with the ui object
    logic = Logic(ui)

    MainWindow.show()
    sys.exit(app.exec())