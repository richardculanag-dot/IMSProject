from IMS import *
# ---------------------------
# Staff Dashboard
# ---------------------------
class StaffDashboard(QWidget):
    def __init__(self, login_widget, username, conn):
        super().__init__()
        self.login_widget = login_widget
        self.username = username
        self.conn = conn
        self.setWindowTitle("Staff")
        self.setWindowIcon(QIcon("images/compforgelogobgremoved.png"))
        self.setGeometry(10, 35, 1350, 650)
        self.setFixedSize(1350, 650)
        self.setStyleSheet("background-color:rgb( 40, 40, 40); border-radius: 10px;")

        self.buttonPanel = QWidget(self)
        self.buttonPanel.setGeometry(10, 10, 160, 630)
        self.buttonPanel.setStyleSheet("background-color: rgb(70, 70, 70)")
        self.buttonPanel.show()

        image_widget = QLabel(self.buttonPanel)
        image_widget.setGeometry(20, 5, 120, 120)
        logo = QPixmap("images/compforgelogobgremoved.png")
        image_widget.setPixmap(logo)
        image_widget.setScaledContents(True)
        image_widget.show()

        self.button_group = ButtonGroupManager()

        self.dashboard_btn = CustomButton(
            "Dashboard", self.buttonPanel,
            "rgb(60, 146, 193)", "cyan", "cyan", self.button_group
        )
        self.dashboard_btn.setGeometry(20, 150, 120, 40)

        self.inventory_btn = CustomButton(
            "Inventory", self.buttonPanel,
            "rgb(60, 146, 193)", "cyan", "cyan", self.button_group
        )
        self.inventory_btn.setGeometry(20, 230, 120, 40)

        self.category_btn = CustomButton(
            "Category", self.buttonPanel,
            "rgb(60, 146, 193)", "cyan", "cyan", self.button_group
        )
        self.category_btn.setGeometry(20, 310, 120, 40)

        self.history_btn = CustomButton(
            "History", self.buttonPanel,
            "rgb(60, 146, 193)", "cyan", "cyan", self.button_group
        )
        self.history_btn.setGeometry(20, 390, 120, 40)

        self.account_btn = CustomButton(
            "Account", self.buttonPanel,
            "rgb(60, 146, 193)", "cyan", "cyan", self.button_group
        )
        self.account_btn.setGeometry(20, 470, 120, 40)
        self.account_btn.clicked.connect(self.show_account_details)


        self.back_btn = CustomButton(
            "←", self.buttonPanel,
            "rgb(70, 70, 70)", "rgb(40,40,40)", "rgb(40,40,40)", self.button_group,
            text_color="rgb(60, 146, 193)", font_size=40
        )
        self.back_btn.setGeometry(20, 580, 50, 40)
        self.back_btn.clicked.connect(self.handle_back_btn_click)

        self.topPanel = QWidget(self)
        self.topPanel.setGeometry(180, 10, 1160, 100)
        self.topPanel.setStyleSheet("background-color: rgb(70, 70, 70)")
        self.topPanel.show()

        self.analyticPanel = QWidget(self)
        self.analyticPanel.setGeometry(180, 120, 1160, 520)
        self.analyticPanel.setStyleSheet("background-color: rgb(70, 70, 70)")
        self.analyticPanel.show()


    def handle_back_btn_click(self, event):

        msg = QMessageBox(self)
        msg.setWindowTitle("Confirm Logout")
        msg.setText("Are you sure you want to log out?\nYou will be returned to the login screen.")
        msg.setIcon(QMessageBox.Icon.Question)

        logout_btn = msg.addButton("Logout", QMessageBox.ButtonRole.YesRole)
        cancel_btn = msg.addButton("Cancel", QMessageBox.ButtonRole.NoRole)

        msg.setDefaultButton(cancel_btn)
        msg.exec()

        if msg.clickedButton() == logout_btn:
            self.close()
            self.login_widget.setVisible(True)

    def show_account_details(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "SELECT username, fname, lname, role FROM accounts WHERE username=%s",
                (self.username,)
            )
            result = cursor.fetchone()
            cursor.close()

            if result:
                uname, fname, lname, role = result

                uname_label = QLabel(f"Username: {uname}", self.analyticPanel)
                fname_label = QLabel(f"First Name: {fname}", self.analyticPanel)
                lname_label = QLabel(f"Last Name: {lname}", self.analyticPanel)
                role_label = QLabel(f"Role: {role}", self.analyticPanel)

                uname_label.setGeometry(20, 20, 300, 40)
                fname_label.setGeometry(20, 60, 300, 40)
                lname_label.setGeometry(20, 100, 300, 40)
                role_label.setGeometry(20, 140, 300, 40)

                uname_label.setStyleSheet("color: white; font-size: 18px;")
                fname_label.setStyleSheet("color: white; font-size: 18px;")
                lname_label.setStyleSheet("color: white; font-size: 18px;")
                role_label.setStyleSheet("color: white; font-size: 18px;")

                uname_label.show()
                fname_label.show()
                lname_label.show()
                role_label.show()

            else:
                QMessageBox.information(self, "Account Details", "Account details not found.")
        except Exception as e:
            QMessageBox.critical(self, "Database Error", str(e))
