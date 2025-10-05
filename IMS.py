import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import Qt
from Staff import *
from Admin import *
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
    def __init__(self, text, parent, normal_color, hover_color, click_color, group_manager, text_color="black",
                 font_size=14):
        super().__init__(text, parent)
        self.normal_color = normal_color
        self.hover_color = hover_color
        self.click_color = click_color
        self.text_color = text_color
        self.font_size = font_size
        self.group_manager = group_manager
        self.selected = False
        self.setStyleSheet(
            f"background-color: {self.normal_color}; color: {self.text_color}; font-size: {self.font_size}px;")
        self._hovered = False

    def enterEvent(self, event):
        if not self.selected:
            self.setStyleSheet(
                f"background-color: {self.hover_color}; color: {self.text_color}; font-size: {self.font_size}px;")
        self._hovered = True

    def leaveEvent(self, event):
        if not self.selected:
            self.setStyleSheet(
                f"background-color: {self.normal_color}; color: {self.text_color}; font-size: {self.font_size}px;")
        self._hovered = False

    def mousePressEvent(self, event):
        self.group_manager.select(self)
        super().mousePressEvent(event)

    def set_selected(self, selected):
        self.selected = selected
        if selected:
            self.setStyleSheet(
                f"background-color: {self.click_color}; color: {self.text_color}; font-size: {self.font_size}px;")
        else:
            self.setStyleSheet(
                f"background-color: {self.normal_color}; color: {self.text_color}; font-size: {self.font_size}px;")

    def deselect(self):
        self.set_selected(False)


# ---------------------------
# Login Widget
# ---------------------------
class LoginWidget(QWidget):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn
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

        image_label = QLabel("CompForge", self)
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
            cursor = self.conn.cursor()
            cursor.execute(
                "SELECT role FROM accounts WHERE username=%s AND password=%s",
                (username, password)
            )
            result = cursor.fetchone()
            print("Query result:", result)

            cursor.close()

            if result:
                role = result[0]
                if role == "Admin":
                    self.admin_dashboard = AdminDashboard(self, username, self.conn)
                    self.admin_dashboard.show()
                    self.setVisible(False)
                elif role == "Staff":
                    self.staff_dashboard = StaffDashboard(self, username, self.conn)
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
    print("Connecting...")
    conn = pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password="",
        database="ims"
    )
    print("Connected!")

    login = LoginWidget(conn)
    login.show()
    exit_code = app.exec()

    conn.close()

    sys.exit(exit_code)
