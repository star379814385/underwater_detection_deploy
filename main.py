import sys
from main_window import URPC_Window, QtWidgets

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = URPC_Window()
    window.show()
    sys.exit(app.exec_())
