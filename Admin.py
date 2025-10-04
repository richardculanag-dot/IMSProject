from IMS import *
# ---------------------------
# Admin Dashboard
# ---------------------------
class AdminDashboard(QWidget):
    def __init__(self, login_widget, username, conn):
        super().__init__()
        self.login_widget = login_widget
        self.username = username
        self.conn = conn
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

