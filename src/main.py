from PySide6 import QtCore, QtGui, QtWidgets


from adminWindowUi import Ui_MainWindow
from adminWindowUi import Ui_MainWindow
from catalogueUI import Ui_Form



class AdminWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(AdminWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setupPages()

    def setupPages(self):
        self.cataloguePage = QtWidgets.QWidget()
        self.cataloguePage.ui = Ui_Form()
        self.cataloguePage.setObjectName("cataloguePage")
        self.cataloguePage.ui.setupUi(self.cataloguePage)
        self.ui.stackedWidget.addWidget(self.cataloguePage)



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    root = AdminWindow()
    root.show()
    sys.exit(app.exec())