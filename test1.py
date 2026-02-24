from PyQt6 import QtCore, QtGui, QtWidgets


class CatalogueForm(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setupUi()

    def setupUi(self):
        self.horizontalLayoutWidget = QtWidgets.QWidget(parent=self)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 1041, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.menuBar1 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.menuBar1.setContentsMargins(0, 0, 0, 0)
        self.menuBar1.setObjectName("menuBar1")
        self.productsButton = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget)
        self.productsButton.setObjectName("productsButton")
        self.menuBar1.addWidget(self.productsButton)
        self.categoriesButton = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget)
        self.categoriesButton.setObjectName("categoriesButton")
        self.menuBar1.addWidget(self.categoriesButton)
        self.salesButton = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget)
        self.salesButton.setObjectName("salesButton")
        self.menuBar1.addWidget(self.salesButton)
        spacerItem = QtWidgets.QSpacerItem(600, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.menuBar1.addItem(spacerItem)
        self.verticalLayoutWidget = QtWidgets.QWidget(parent=self)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 50, 1021, 821))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.allSmthLabel = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(22)
        self.allSmthLabel.setFont(font)
        self.allSmthLabel.setObjectName("allSmthLabel")
        self.verticalLayout.addWidget(self.allSmthLabel)
        self.searchLabel = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.searchLabel.setFont(font)
        self.searchLabel.setObjectName("searchLabel")
        self.verticalLayout.addWidget(self.searchLabel)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.searchEdit = QtWidgets.QLineEdit(parent=self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.searchEdit.setFont(font)
        self.searchEdit.setObjectName("searchEdit")
        self.horizontalLayout.addWidget(self.searchEdit)
        self.searchButton = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.searchButton.setObjectName("searchButton")
        self.horizontalLayout.addWidget(self.searchButton)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.addButton = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.addButton.setObjectName("addButton")
        self.horizontalLayout.addWidget(self.addButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tableView = QtWidgets.QTableView(parent=self.verticalLayoutWidget)
        self.tableView.setObjectName("tableView")
        self.verticalLayout.addWidget(self.tableView)

        self.set_text()

        self.categoriesButton.clicked.connect(self.on_categoriesButton_clicked)
        self.productsButton.clicked.connect(self.on_productsButton_clicked)
        self.salesButton.clicked.connect(self.on_salesButton_clicked)

    def set_text(self):
        #Form.setWindowTitle("Desktop"))
        self.productsButton.setText("Изделия")
        self.categoriesButton.setText("Категории изделий")
        self.salesButton.setText("Акции на изделия")
        self.allSmthLabel.setText("Все изделия")
        self.searchLabel.setText("Поиск по артикулу или наименованию")
        self.searchButton.setText("Поиск")
        self.addButton.setText("+")

    def on_categoriesButton_clicked(self):
        self.allSmthLabel.setText("Все категории")
        self.searchLabel.setText("Поиск по наименованию категории")

    def on_productsButton_clicked(self):

        self.allSmthLabel.setText("Все изделия")
        self.searchLabel.setText("Поиск по артикулу или наименованию")

    def on_salesButton_clicked(self):

        self.allSmthLabel.setText("Все акции")
        self.searchLabel.setText("Поиск по наименованию акции")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    root = CatalogueForm()
    root.show()
    sys.exit(app.exec())
