from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
    QFrame, QGridLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QTextEdit, QVBoxLayout,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setEnabled(True)
        Dialog.resize(700, 818)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(700, 688))
        Dialog.setMaximumSize(QSize(700, 1000))
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(32)
        self.gridLayout.setVerticalSpacing(15)
        self.gridLayout.setContentsMargins(10, -1, 10, -1)
        self.uglevodiEdit = QLineEdit(Dialog)
        self.uglevodiEdit.setObjectName(u"uglevodiEdit")
        self.uglevodiEdit.setMaximumSize(QSize(350, 30))
        font = QFont()
        font.setFamilies([u"Bahnschrift"])
        font.setPointSize(14)
        self.uglevodiEdit.setFont(font)

        self.gridLayout.addWidget(self.uglevodiEdit, 17, 1, 1, 1)

        self.productSelfpriceEdit = QLineEdit(Dialog)
        self.productSelfpriceEdit.setObjectName(u"productSelfpriceEdit")
        self.productSelfpriceEdit.setMaximumSize(QSize(350, 30))
        self.productSelfpriceEdit.setFont(font)

        self.gridLayout.addWidget(self.productSelfpriceEdit, 5, 1, 1, 1)

        self.addSmthLabel = QLabel(Dialog)
        self.addSmthLabel.setObjectName(u"addSmthLabel")
        self.addSmthLabel.setMaximumSize(QSize(350, 30))
        font1 = QFont()
        font1.setFamilies([u"Bahnschrift"])
        font1.setPointSize(24)
        font1.setBold(True)
        self.addSmthLabel.setFont(font1)

        self.gridLayout.addWidget(self.addSmthLabel, 0, 0, 1, 2)

        self.categoriesComboBox = QComboBox(Dialog)
        self.categoriesComboBox.setObjectName(u"categoriesComboBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.categoriesComboBox.sizePolicy().hasHeightForWidth())
        self.categoriesComboBox.setSizePolicy(sizePolicy1)
        self.categoriesComboBox.setMaximumSize(QSize(350, 30))
        self.categoriesComboBox.setFont(font)

        self.gridLayout.addWidget(self.categoriesComboBox, 3, 1, 1, 1)

        self.uglevodiLabel = QLabel(Dialog)
        self.uglevodiLabel.setObjectName(u"uglevodiLabel")
        self.uglevodiLabel.setMaximumSize(QSize(350, 20))
        font2 = QFont()
        font2.setFamilies([u"Bahnschrift"])
        font2.setPointSize(16)
        self.uglevodiLabel.setFont(font2)

        self.gridLayout.addWidget(self.uglevodiLabel, 16, 1, 1, 1)

        self.productPriceEdit = QLineEdit(Dialog)
        self.productPriceEdit.setObjectName(u"productPriceEdit")
        self.productPriceEdit.setMaximumSize(QSize(350, 30))
        self.productPriceEdit.setFont(font)

        self.gridLayout.addWidget(self.productPriceEdit, 5, 0, 1, 1)

        self.categoryLabel = QLabel(Dialog)
        self.categoryLabel.setObjectName(u"categoryLabel")
        self.categoryLabel.setMaximumSize(QSize(350, 20))
        self.categoryLabel.setFont(font2)

        self.gridLayout.addWidget(self.categoryLabel, 2, 1, 1, 1)

        self.belkiEdit = QLineEdit(Dialog)
        self.belkiEdit.setObjectName(u"belkiEdit")
        self.belkiEdit.setMaximumSize(QSize(350, 30))
        self.belkiEdit.setFont(font)

        self.gridLayout.addWidget(self.belkiEdit, 15, 1, 1, 1)

        self.contentTextEdit = QTextEdit(Dialog)
        self.contentTextEdit.setObjectName(u"contentTextEdit")

        self.gridLayout.addWidget(self.contentTextEdit, 10, 0, 1, 2)

        self.descriptionLabel = QLabel(Dialog)
        self.descriptionLabel.setObjectName(u"descriptionLabel")
        self.descriptionLabel.setMaximumSize(QSize(350, 20))
        self.descriptionLabel.setFont(font2)

        self.gridLayout.addWidget(self.descriptionLabel, 6, 0, 1, 1)

        self.okButton = QPushButton(Dialog)
        self.okButton.setObjectName(u"okButton")
        self.okButton.setMaximumSize(QSize(350, 30))
        self.okButton.setFont(font2)

        self.gridLayout.addWidget(self.okButton, 20, 0, 1, 1)

        self.energyvalueLabel = QLabel(Dialog)
        self.energyvalueLabel.setObjectName(u"energyvalueLabel")
        self.energyvalueLabel.setMaximumSize(QSize(350, 20))
        self.energyvalueLabel.setFont(font2)

        self.gridLayout.addWidget(self.energyvalueLabel, 13, 0, 1, 1)

        self.zhiriEdit = QLineEdit(Dialog)
        self.zhiriEdit.setObjectName(u"zhiriEdit")
        self.zhiriEdit.setMaximumSize(QSize(350, 30))
        self.zhiriEdit.setFont(font)

        self.gridLayout.addWidget(self.zhiriEdit, 17, 0, 1, 1)

        self.productSelfpriceLabel = QLabel(Dialog)
        self.productSelfpriceLabel.setObjectName(u"productSelfpriceLabel")
        self.productSelfpriceLabel.setMaximumSize(QSize(350, 20))
        self.productSelfpriceLabel.setFont(font2)

        self.gridLayout.addWidget(self.productSelfpriceLabel, 4, 1, 1, 1)

        self.productNameEdit = QLineEdit(Dialog)
        self.productNameEdit.setObjectName(u"productNameEdit")
        self.productNameEdit.setEnabled(True)
        self.productNameEdit.setMaximumSize(QSize(350, 30))
        self.productNameEdit.setFont(font)

        self.gridLayout.addWidget(self.productNameEdit, 3, 0, 1, 1)

        self.productNameLabel = QLabel(Dialog)
        self.productNameLabel.setObjectName(u"productNameLabel")
        self.productNameLabel.setMaximumSize(QSize(350, 20))
        font3 = QFont()
        font3.setFamilies([u"Bahnschrift"])
        font3.setPointSize(16)
        font3.setBold(False)
        self.productNameLabel.setFont(font3)

        self.gridLayout.addWidget(self.productNameLabel, 2, 0, 1, 1)

        self.productPriceLabel = QLabel(Dialog)
        self.productPriceLabel.setObjectName(u"productPriceLabel")
        self.productPriceLabel.setMaximumSize(QSize(350, 20))
        self.productPriceLabel.setFont(font2)

        self.gridLayout.addWidget(self.productPriceLabel, 4, 0, 1, 1)

        self.belkiLabel = QLabel(Dialog)
        self.belkiLabel.setObjectName(u"belkiLabel")
        self.belkiLabel.setMaximumSize(QSize(350, 20))
        self.belkiLabel.setFont(font2)

        self.gridLayout.addWidget(self.belkiLabel, 13, 1, 1, 1)

        self.energyvalueEdit = QLineEdit(Dialog)
        self.energyvalueEdit.setObjectName(u"energyvalueEdit")
        self.energyvalueEdit.setMaximumSize(QSize(350, 30))
        self.energyvalueEdit.setFont(font)

        self.gridLayout.addWidget(self.energyvalueEdit, 15, 0, 1, 1)

        self.discardButton = QPushButton(Dialog)
        self.discardButton.setObjectName(u"discardButton")
        self.discardButton.setMaximumSize(QSize(350, 30))
        self.discardButton.setFont(font2)

        self.gridLayout.addWidget(self.discardButton, 20, 1, 1, 1)

        self.zhiriLabel = QLabel(Dialog)
        self.zhiriLabel.setObjectName(u"zhiriLabel")
        self.zhiriLabel.setMaximumSize(QSize(350, 20))
        self.zhiriLabel.setFont(font2)

        self.gridLayout.addWidget(self.zhiriLabel, 16, 0, 1, 1)

        self.descriptionTextEdit = QTextEdit(Dialog)
        self.descriptionTextEdit.setObjectName(u"descriptionTextEdit")
        self.descriptionTextEdit.setMaximumSize(QSize(700, 200))
        font4 = QFont()
        font4.setPointSize(12)
        self.descriptionTextEdit.setFont(font4)

        self.gridLayout.addWidget(self.descriptionTextEdit, 8, 0, 1, 2)

        self.line = QFrame(Dialog)
        self.line.setObjectName(u"line")
        font5 = QFont()
        font5.setFamilies([u"Arial"])
        font5.setPointSize(36)
        font5.setBold(True)
        self.line.setFont(font5)
        self.line.setFrameShadow(QFrame.Shadow.Plain)
        self.line.setLineWidth(1)
        self.line.setFrameShape(QFrame.Shape.HLine)

        self.gridLayout.addWidget(self.line, 1, 0, 1, 2)

        self.contentLabel = QLabel(Dialog)
        self.contentLabel.setObjectName(u"contentLabel")
        self.contentLabel.setFont(font2)

        self.gridLayout.addWidget(self.contentLabel, 9, 0, 1, 2)

        self.line_2 = QFrame(Dialog)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShadow(QFrame.Shadow.Plain)
        self.line_2.setFrameShape(QFrame.Shape.HLine)

        self.gridLayout.addWidget(self.line_2, 19, 0, 1, 2)

        self.picInsertButton = QPushButton(Dialog)
        self.picInsertButton.setObjectName(u"picInsertButton")
        self.picInsertButton.setMaximumSize(QSize(350, 16777215))
        self.picInsertButton.setFont(font2)

        self.gridLayout.addWidget(self.picInsertButton, 18, 1, 1, 1)

        self.checkBox = QCheckBox(Dialog)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setFont(font2)
        self.checkBox.setIconSize(QSize(20, 20))
        self.checkBox.setChecked(False)
        self.checkBox.setTristate(False)

        self.gridLayout.addWidget(self.checkBox, 18, 0, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.addSmthLabel.setText(QCoreApplication.translate("Dialog", u"\u0418\u0437\u0434\u0435\u043b\u0438\u0435: name", None))
        self.uglevodiLabel.setText(QCoreApplication.translate("Dialog", u"\u0423\u0433\u043b\u0435\u0432\u043e\u0434\u044b \u0433.:", None))
        self.categoryLabel.setText(QCoreApplication.translate("Dialog", u"\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f:", None))
        self.descriptionLabel.setText(QCoreApplication.translate("Dialog", u"\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u0438\u0437\u0434\u0435\u043b\u0438\u044f", None))
        self.okButton.setText(QCoreApplication.translate("Dialog", u"\u041e\u043a", None))
        self.energyvalueLabel.setText(QCoreApplication.translate("Dialog", u"\u042d\u043d\u0435\u0440\u0433\u0435\u0442\u0438\u0447\u0435\u0441\u043a\u0430\u044f \u0446\u0435\u043d\u043d\u043e\u0441\u0442\u044c \u043a\u0430\u043b.:", None))
        self.productSelfpriceLabel.setText(QCoreApplication.translate("Dialog", u"\u0421\u0435\u0431\u0435\u0441\u0442\u043e\u0438\u043c\u043e\u0441\u0442\u044c \u0438\u0437\u0434\u0435\u043b\u0438\u044f \u0440\u0443\u0431.:", None))
        self.productNameLabel.setText(QCoreApplication.translate("Dialog", u"\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435 \u0438\u0437\u0434\u0435\u043b\u0438\u044f:", None))
        self.productPriceLabel.setText(QCoreApplication.translate("Dialog", u"\u0426\u0435\u043d\u0430 \u0438\u0437\u0434\u0435\u043b\u0438\u044f \u0440\u0443\u0431.:", None))
        self.belkiLabel.setText(QCoreApplication.translate("Dialog", u"\u0411\u0435\u043b\u043a\u0438 \u0433.:", None))
        self.discardButton.setText(QCoreApplication.translate("Dialog", u"\u041e\u0442\u043c\u0435\u043d\u0430", None))
        self.zhiriLabel.setText(QCoreApplication.translate("Dialog", u"\u0416\u0438\u0440\u044b \u0433.:", None))
        self.descriptionTextEdit.setHtml(QCoreApplication.translate("Dialog", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">fffffff</p></body></html>", None))
        self.contentLabel.setText(QCoreApplication.translate("Dialog", u"\u0421\u043e\u0441\u0442\u0430\u0432 \u0438\u0437\u0434\u0435\u043b\u0438\u044f", None))
        self.picInsertButton.setText(QCoreApplication.translate("Dialog", u"\u0417\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044c \u0444\u043e\u0442\u043e\u0433\u0440\u0430\u0444\u0438\u044e \u0438\u0437\u0434\u0435\u043b\u0438\u044f", None))
        self.checkBox.setText(QCoreApplication.translate("Dialog", u"\u041e\u0442\u043e\u0431\u0440\u0430\u0436\u0430\u0442\u044c \u0438\u0437\u0434\u0435\u043b\u0438\u0435", None))
    # retranslateUi

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = QDialog()
    ui = Ui_Dialog()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())