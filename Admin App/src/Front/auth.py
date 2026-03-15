import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView,
    QLabel, QFrame, QDialog, QGridLayout, QComboBox, QMessageBox,
    QDialogButtonBox, QGroupBox, QStackedWidget, QTabWidget, QListWidget,
    QListWidgetItem, QTextEdit, QDateEdit, QSpinBox, QDoubleSpinBox,
    QCheckBox, QRadioButton, QButtonGroup, QSplitter, QTreeWidget,
    QTreeWidgetItem, QProgressBar, QSlider, QDial
)
from PySide6.QtCore import Qt, QSize, Signal, QDate, QTimer
from PySide6.QtGui import QFont, QColor, QIcon, QPixmap, QPainter, QPen
from PySide6.QtCharts import QChart, QChartView, QPieSeries, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
import random
from datetime import datetime, timedelta


class LoginScreen(QMainWindow):
    #Сигнал для перехода к основному приложению после авторизации
    login_successful = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Панель администратора")
        self.setMinimumSize(1200, 600)

        #Устанавливаем центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        #Основной layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(400, 40, 400, 100)
        main_layout.setSpacing(15)

        #Заголовок
        self.create_title(main_layout)

        #Форма авторизации
        self.create_login_form(main_layout)

        #Кнопка входа
        self.create_login_button(main_layout)

    def create_title(self, layout):
        title = QLabel("Вход в систему")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                font-size: 35px;
                font-weight: bold;
                color: #0078d7;
                margin-bottom: 20px;
            }
        """)
        layout.addWidget(title)

    def create_login_form(self, layout):
        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        form_layout.setContentsMargins(0, 0, 0, 0)

        #Поле логина
        login_label = QLabel("Логин сотрудника")
        login_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #333;
                padding: 0px;
                margin: 0px;
            }
        """)
        form_layout.addWidget(login_label)

        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Введите логин")
        self.login_input.setFixedHeight(35)
        self.login_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #ddd;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 14px;
                background-color: white;
                margin: 0px;
            }
            QLineEdit:focus {
                border-color: #0078d7;
            }
        """)
        form_layout.addWidget(self.login_input)

        #Поле пароля
        password_label = QLabel("Пароль сотрудника")
        password_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #333;
                padding: 0px;
                margin: 0px;
            }
        """)
        form_layout.addWidget(password_label)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Введите пароль")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedHeight(35)
        self.password_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #ddd;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 14px;
                background-color: white;
                margin: 0px;
            }
            QLineEdit:focus {
                border-color: #0078d7;
            }
        """)
        form_layout.addWidget(self.password_input)

        layout.addWidget(form_widget)

    def create_login_button(self, layout):
        self.login_button = QPushButton("Авторизоваться")
        self.login_button.setFixedHeight(40)
        self.login_button.setCursor(Qt.PointingHandCursor)
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #0078d7;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
                margin-top: 5px;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
            QPushButton:pressed {
                background-color: #004080;
            }
        """)
        self.login_button.clicked.connect(self.authenticate)

        self.login_input.returnPressed.connect(self.authenticate)
        self.password_input.returnPressed.connect(self.authenticate)

        layout.addWidget(self.login_button)

    def authenticate(self):
        login = self.login_input.text().strip()
        password = self.password_input.text()

        if login == "":
            QMessageBox.warning(self, "Ошибка", "Введите логин")
            self.login_input.setFocus()
            return

        if password == "":
            QMessageBox.warning(self, "Ошибка", "Введите пароль")
            self.password_input.setFocus()
            return

        #Учётки для входа
        valid_credentials = {
            "admin": "admin123"
        }

        if login in valid_credentials and valid_credentials[login] == password:
            self.login_successful.emit()
            self.close()
        else:
            QMessageBox.critical(
                self,
                "Ошибка авторизации",
                "Неверный логин или пароль."
            )
            self.password_input.clear()
            self.password_input.setFocus()


class MainApplication(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Панель администратора")
        self.setMinimumSize(1200, 600)


class ApplicationController:
    def __init__(self):
        self.app = QApplication(sys.argv)

        self.login_window = LoginScreen()
        self.login_window.login_successful.connect(self.show_main_window)

        self.main_window = None

    def show_main_window(self):
        self.main_window = MainApplication()
        self.main_window.show()

    def run(self):
        self.login_window.show()
        return self.app.exec()


def main():
    controller = ApplicationController()
    sys.exit(controller.run())


if __name__ == "__main__":
    main()