import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import Qt
# import mysql.connector
from mysql.connector import Error
import pymysql


class ButtonGroupManager:
    def __init__(self):
        self.selected_button = None

    def select(self, button):
        if self.selected_button and self.selected_button is not button:
            self.selected_button.deselect()
        self.selected_button = button
        button.set_selected(True)

class CustomButton(QPushButton):
    def __init__(self, text, parent, normal_color, hover_color, click_color, group_manager, text_color="black", font_size=14):
        super().__init__(text, parent)
        self.normal_color = normal_color
        self.hover_color = hover_color
        self.click_color = click_color
        self.text_color = text_color
        self.font_size = font_size
        self.group_manager = group_manager
        self.selected = False
        self.setStyleSheet(f"background-color: {self.normal_color}; color: {self.text_color}; font-size: {self.font_size}px;")
        self._hovered = False

    def enterEvent(self, event):
        if not self.selected:
            self.setStyleSheet(f"background-color: {self.hover_color}; color: {self.text_color}; font-size: {self.font_size}px;")
        self._hovered = True

    def leaveEvent(self, event):
        if not self.selected:
            self.setStyleSheet(f"background-color: {self.normal_color}; color: {self.text_color}; font-size: {self.font_size}px;")
        self._hovered = False

    def mousePressEvent(self, event):
        self.group_manager.select(self)
        super().mousePressEvent(event)

    def set_selected(self, selected):
        self.selected = selected
        if selected:
            self.setStyleSheet(f"background-color: {self.click_color}; color: {self.text_color}; font-size: {self.font_size}px;")
        else:
            self.setStyleSheet(f"background-color: {self.normal_color}; color: {self.text_color}; font-size: {self.font_size}px;")

    def deselect(self):
        self.set_selected(False)

# ---------------------------
# Admin Dashboard
# ---------------------------
class AdminDashboard(QWidget):
    def __init__(self, login_widget, username):
        super().__init__()
        self.login_widget = login_widget
        self.username = username
        self.setWindowTitle("Admin")
        self.setWindowIcon(QIcon("images/compforgelogobgremoved.png"))
        self.setGeometry(10, 35, 1350, 650)
        self.setFixedSize(1350, 650)
        self.setStyleSheet("background-color:rgb( 40, 40, 40); border-radius: 10px;")

        buttonPanel = QWidget(self)
        buttonPanel.setGeometry(10, 10, 160, 630)
        buttonPanel.setStyleSheet("background-color: rgb(70, 70, 70)")
        buttonPanel.show()

        image_widget = QLabel(buttonPanel)
        image_widget.setGeometry(20, 5, 120, 120)
        logo = QPixmap("images/compforgelogobgremoved.png")
        image_widget.setPixmap(logo)
        image_widget.setScaledContents(True)
        image_widget.show()

        self.button_group = ButtonGroupManager()

        self.dashboard_btn = CustomButton(
            "Dashboard", buttonPanel,
            "rgb(60, 146, 193)", "cyan", "cyan", self.button_group
        )
        self.dashboard_btn.setGeometry(20, 150, 120, 40)

        self.reports_btn = CustomButton(
            "Reports", buttonPanel,
            "rgb(60, 146, 193)", "cyan", "cyan", self.button_group
        )
        self.reports_btn.setGeometry(20, 230, 120, 40)

        self.users_btn = CustomButton(
            "Users", buttonPanel,
            "rgb(60, 146, 193)", "cyan", "cyan", self.button_group
        )
        self.users_btn.setGeometry(20, 310, 120, 40)

        self.logs_btn = CustomButton(
            "Logs", buttonPanel,
            "rgb(60, 146, 193)", "cyan", "cyan", self.button_group
        )
        self.logs_btn.setGeometry(20, 390, 120, 40)

        self.back_btn = CustomButton(
            "←", buttonPanel,
            "rgb(70, 70, 70)", "rgb(40,40,40)", "rgb(40,40,40)", self.button_group,
            text_color="rgb(60, 146, 193)", font_size=40
        )
        self.back_btn.setGeometry(20, 580, 50, 40)
        self.back_btn.mousePressEvent = self.handle_back_btn_click

        topPanel = QWidget(self)
        topPanel.setGeometry(180, 10, 1160, 100)
        topPanel.setStyleSheet("background-color: rgb(70, 70, 70)")
        topPanel.show()

        analyticPanel = QWidget(self)
        analyticPanel.setGeometry(180, 120, 1160, 520)
        analyticPanel.setStyleSheet("background-color: rgb(70, 70, 70)")
        analyticPanel.show()

    def handle_back_btn_click(self, event):
        reply = QMessageBox.question(
            self, "Logout?", "Logout?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.close()
            self.login_widget.setVisible(True)
# ---------------------------
# Staff Dashboard
# ---------------------------
class StaffDashboard(QWidget):
    def __init__(self, login_widget, username):
        super().__init__()
        self.login_widget = login_widget
        self.username = username
        self.setWindowTitle("Staff")
        self.setWindowIcon(QIcon("images/compforgelogobgremoved.png"))
        self.setGeometry(10, 35, 1350, 650)
        self.setFixedSize(1350, 650)
        self.setStyleSheet("background-color:rgb( 40, 40, 40); border-radius: 10px;")

        buttonPanel = QWidget(self)
        buttonPanel.setGeometry(10, 10, 160, 630)
        buttonPanel.setStyleSheet("background-color: rgb(70, 70, 70)")
        buttonPanel.show()

        image_widget = QLabel(buttonPanel)
        image_widget.setGeometry(20, 5, 120, 120)
        logo = QPixmap("images/compforgelogobgremoved.png")
        image_widget.setPixmap(logo)
        image_widget.setScaledContents(True)
        image_widget.show()

        self.button_group = ButtonGroupManager()

        self.dashboard_btn = CustomButton(
            "Dashboard", buttonPanel,
            "rgb(60, 146, 193)", "cyan", "cyan", self.button_group
        )
        self.dashboard_btn.setGeometry(20, 150, 120, 40)

        self.inventory_btn = CustomButton(
            "Inventory", buttonPanel,
            "rgb(60, 146, 193)", "cyan", "cyan", self.button_group
        )
        self.inventory_btn.setGeometry(20, 230, 120, 40)

        self.category_btn = CustomButton(
            "Category", buttonPanel,
            "rgb(60, 146, 193)", "cyan", "cyan", self.button_group
        )
        self.category_btn.setGeometry(20, 310, 120, 40)

        self.history_btn = CustomButton(
            "History", buttonPanel,
            "rgb(60, 146, 193)", "cyan", "cyan", self.button_group
        )
        self.history_btn.setGeometry(20, 390, 120, 40)

        self.account_btn = CustomButton(
            "Account", buttonPanel,
            "rgb(60, 146, 193)", "cyan", "cyan", self.button_group
        )
        self.account_btn.setGeometry(20, 470, 120, 40)
        self.account_btn.clicked.connect(self.show_account_details)

        self.back_btn = CustomButton(
            "←", buttonPanel,
            "rgb(70, 70, 70)", "rgb(40,40,40)", "rgb(40,40,40)", self.button_group,
            text_color="rgb(60, 146, 193)", font_size=40
        )
        self.back_btn.setGeometry(20, 580, 50, 40)
        self.back_btn.mousePressEvent = self.handle_back_btn_click

        topPanel = QWidget(self)
        topPanel.setGeometry(180, 10, 1160, 100)
        topPanel.setStyleSheet("background-color: rgb(70, 70, 70)")
        topPanel.show()

        analyticPanel = QWidget(self)
        analyticPanel.setGeometry(180, 120, 1160, 520)
        analyticPanel.setStyleSheet("background-color: rgb(70, 70, 70)")
        analyticPanel.show()

    def handle_back_btn_click(self, event):
        reply = QMessageBox.question(
            self, "Logout?", "Logout?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.close()
            self.login_widget.setVisible(True)
    def show_account_details(self):
        try:
            conn = pymysql.connect(
                host='localhost',
                port=3360,
                user='root',
                password='',
                database='ims'
            )
            cursor = conn.cursor()
            cursor.execute(
                "SELECT username, fname, lname, role FROM accounts WHERE username=%s",
                (self.username,)
            )
            result = cursor.fetchone()
            cursor.close()
            conn.close()

            if result:
                uname, fname, lname, role = result
                details = f"Username: {uname}\nFirst Name: {fname}\nLast Name: {lname}\nRole: {role}"
            else:
                details = "Account details not found."

            QMessageBox.information(self, "Account Details", details)
        except Exception as e:
            QMessageBox.critical(self, "Database Error", str(e))

# ---------------------------
# Login Widget
# ---------------------------
class LoginWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CompForge")
        self.setWindowIcon(QIcon("images/compforgelogobgremoved.png"))
        self.setGeometry(540, 200, 350, 400)
        self.role_label = QLabel("Username:", self)
        self.role_label.setGeometry(148, 160, 100, 30)
        self.setStyleSheet("background-color:rgb( 40, 40, 40);")
        self.setFixedSize(350, 400)

        self.role_input = QLineEdit(self)
        self.role_input.setPlaceholderText("Enter username")
        self.role_input.setStyleSheet("background-color: rgb(60, 146, 193); color: black;")
        self.role_input.setGeometry(88, 185, 180, 30)

        # Password
        self.password_label = QLabel("Password:", self)
        self.password_label.setGeometry(150, 225, 100, 30)

        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setStyleSheet("background-color: rgb(60, 146, 193); color: black;")
        self.password_input.setGeometry(88, 250, 180, 30)

        # Login button
        self.login_button = QPushButton("Login", self)
        self.login_button.setGeometry(88, 320, 180, 35)
        self.login_button.clicked.connect(self.handle_login)
        self.login_button.setStyleSheet("background-color:cyan; color: black; font-size: 14px; font-family: Arial")
        self.login_button.setDefault(True)
        self.password_input.returnPressed.connect(self.handle_login)

        # CheckBox password
        self.show_password_cb = QCheckBox("Show Password", self)
        self.show_password_cb.setGeometry(130, 285, 150, 20)
        self.show_password_cb.setStyleSheet("color: white; font-size: 10px")
        self.show_password_cb.stateChanged.connect(self.toggle_password_visibility)

        image_label = QLabel("CompForge",self)
        image_label.setStyleSheet("color:rgb(60, 146, 193); font-weight: bold; font-family: Burberry;")
        image_label.setGeometry(145, 120, 100, 30)
        image_label.show()

        image_widget = QLabel(self)
        image_widget.setGeometry(118, 10, 120, 120)
        logo = QPixmap("images/compforgelogobgremoved.png")
        image_widget.setPixmap(logo)
        image_widget.setScaledContents(True)
        image_widget.show()

    def handle_login(self):
        username = self.role_input.text()
        password = self.password_input.text()

        try:
            print("Connecting...")
            conn = pymysql.connect(
                host='localhost',
                port=3360,
                user='root',
                password='',
                database='ims'
            )
            print("Connected!")

            cursor = conn.cursor()
            cursor.execute(
                "SELECT role FROM accounts WHERE username=%s AND password=%s",
                (username, password)
            )
            result = cursor.fetchone()
            print("Query result:", result)

            cursor.close()
            conn.close()

            if result:
                role = result[0]
                if role == "Admin":
                    self.admin_dashboard = AdminDashboard(self, username)
                    self.admin_dashboard.show()
                    self.setVisible(False)
                elif role == "Staff":
                    self.staff_dashboard = StaffDashboard(self, username)
                    self.staff_dashboard.show()
                    self.setVisible(False)
            else:
                QMessageBox.warning(self, "Error", "Invalid username or password")

        except Exception as e:
            print("Error:", e)
            QMessageBox.critical(self, "Database Error", str(e))

    def toggle_password_visibility(self, state):
        if state == Qt.CheckState.Checked.value:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

# ---------------------------
# Main Program
# ---------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = LoginWidget()
    login.show()
    sys.exit(app.exec())
