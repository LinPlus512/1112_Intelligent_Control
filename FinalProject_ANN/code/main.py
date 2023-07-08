import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox, QStackedLayout, QComboBox, QLabel
from PyQt6.QtCore import QTimer, QTime
from PyQt6.QtGui import QPixmap, QFont
from predict_function import get_info

class SecondPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.addr, self.current, self.predict, self.tot = get_info()    

        # bg
        background_label = QLabel(self)
        background_label.setGeometry(0, 0, 320, 695)
        pixmap = QPixmap("NN_project/APP_bg_page2.png")  # 將 "background.jpg" 替換為您的背景圖片檔案名稱
        background_label.setPixmap(pixmap)
        background_label.setScaledContents(True)

        # layout = QVBoxLayout()
        back_button = QPushButton("HOME", self)
        back_button.setGeometry(10, 10, 300, 60)  # 設置按鈕的位置和大小

        self.combo_box = QComboBox(self)
        self.combo_box.setGeometry(10, 100, 300, 60)  # 設置下拉式選單的位置和大小
        self.combo_box.setPlaceholderText("SELECT...") 
        self.combo_box.addItems(self.addr)

        # layout.addWidget(self.combo_box)
        # layout.addWidget(back_button)
        back_button.clicked.connect(parent.show_home_page)
        self.combo_box.activated.connect(self.handle_combo_box)

        # time
        self.clock_label = QLabel(self)
        self.clock_label.setGeometry(10, 200, 300, 60)  # 設置標籤的位置和大小
        self.clock_label.setFont(QFont("Arial", 48))  # 設置字型大小

        # layout.addWidget(self.clock_label)

        # value 
        self.tot_label = QLabel(self)
        self.tot_label.setGeometry(10, 300, 300, 60)  # 設置標籤的位置和大小
        self.tot_label.setFont(QFont("Arial", 48))
        self.current_label = QLabel(self)
        self.current_label.setGeometry(10, 400, 300, 60)  # 設置標籤的位置和大小
        self.current_label.setFont(QFont("Arial", 48))
        self.predict_label = QLabel(self)
        self.predict_label.setGeometry(10, 500, 300, 60)  # 設置標籤的位置和大小
        self.predict_label.setFont(QFont("Arial", 48))
        self.tot_label.setText('')
        self.current_label.setText('')
        self.predict_label.setText('')

        # layout.addWidget(self.tot_label)
        # layout.addWidget(self.current_label)
        # layout.addWidget(self.predict_label)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(1000)

        # self.setLayout(layout)

    def update_clock(self):
        current_time = QTime.currentTime()
        display_text = current_time.toString("hh:mm")
        self.clock_label.setText(display_text)
        
    def handle_combo_box(self, index):
        selected_item = self.addr[index]
        _, self.current, self.predict,self.tot = get_info()
        self.update_current_and_predict(index)

    def update_current_and_predict(self, index):
        self.tot_label.setText(f"Total: {self.tot[index]}")
        self.current_label.setText(f"Current: {self.current[index]}")
        self.predict_label.setText(f"Predict: {self.predict[index]}")

class HomePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # layout = QVBoxLayout()
        # bg
        background_label = QLabel(self)
        background_label.setGeometry(0, 0, 320, 695)
        pixmap = QPixmap("NN_project/APP_bg_home.png")  # 將 "background.jpg" 替換為您的背景圖片檔案名稱
        background_label.setPixmap(pixmap)
        background_label.setScaledContents(True)

        second_page_button = QPushButton("START", self)
        second_page_button.setGeometry(10, 250, 300, 60)
        message_box_button = QPushButton("README", self)
        message_box_button.setGeometry(10, 350, 300, 60)
        # layout.addWidget(second_page_button)
        # layout.addWidget(message_box_button)
        # self.setLayout(layout)

        second_page_button.clicked.connect(parent.show_second_page)
        message_box_button.clicked.connect(parent.show_message_box)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(320, 695)
        self.setWindowTitle("Ubike Prediction")
        self.home_page = HomePage(self)
        self.second_page = SecondPage(self)
        self.stacked_widget = QWidget()
        self.stacked_layout = QStackedLayout(self.stacked_widget)
        self.stacked_layout.addWidget(self.home_page)
        self.setCentralWidget(self.stacked_widget)
        self.addr, self.current, self.predict, self.tot = get_info()  
        
    def info(self):
        return get_info()

    def show_second_page(self):
        self.second_page.combo_box.addItems(self.addr) 
        self.second_page.combo_box.setPlaceholderText("SELECT...") 
        self.stacked_layout.addWidget(self.second_page)
        self.stacked_layout.setCurrentIndex(1)
        # self.addr, self.current_sbi, self.predict_sbi = get_info()

    def show_message_box(self):
        QMessageBox.information(self, "README", "Please press START, and the program will start predicting the number of available parking spaces after 30 minutes.")

    def show_home_page(self):
        self.stacked_layout.setCurrentIndex(0)
        self.clear_labels()

    def clear_labels(self):
        self.second_page.combo_box.clear() 
        self.second_page.combo_box.setPlaceholderText("SELECT...") 
        self.second_page.tot_label.setText('')
        self.second_page.current_label.setText('')
        self.second_page.predict_label.setText('')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())
