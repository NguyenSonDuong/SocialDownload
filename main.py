# import ui.controller.uicontroller as controller 
# from config.setting import Setting, Social, TypeChannel, TypeID
# # import time
# # from flask import Flask, request, jsonify
# # from flask_cors import CORS
# # from flask_socketio import SocketIO
# # from config.setting import Setting, TypeDownloadYoutube, TypeID,Social
# # from youtube.youtube import Youtube as yt
# # from douyin.douyin import Douyin as dy

# # app = Flask(__name__)
# # CORS(app)  # Cho phép React truy cập API
# # socketio = SocketIO(app, cors_allowed_origins="*")  # Kích hoạt WebSocket

# # @app.route("/run", methods=["POST"])
# # def download():
# #     data = request.get_json()
# #     if not data:
# #          return jsonify({"error": "No URL provided"}), 400
# #     setting = Setting(**data)

# #     socketio.start_background_task(download_video, setting)
# #     return jsonify({"message": "Kết nối thành công vui lòng chờ...."})

# # def download_video(setting):
# #     try:
# #         socketio.emit("progress", {"status": "Start"})
# #         if setting.social == Social.DOUYIN:
# #             douyin = dy(socketio.emit,setting)
# #             douyin.run()
# #         if setting.social == Social.YOUTUBE:
# #             youtube = yt(socketio.emit,setting)
# #             youtube.run()
# #         if setting.social == Social.WEIBO:
# #             socketio.emit("progress", {"status": "update"})
# #     except Exception as ex:
# #         print(ex)

# # if __name__ == "__main__":
# #     socketio.run(app, port=5000, debug=True)

# while True:
#     url = input("Nhập url:")
#     setting = Setting(social=Social.YOUTUBE, type_id=TypeID.CHANNEL)
#     print(controller.validateUrlYoutube(url,setting))

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QDialog
from PyQt5.QtCore import Qt

class OverlayDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Overlay Dialog")
        self.setWindowModality(Qt.ApplicationModal)  # Chặn tương tác với cửa sổ chính khi overlay xuất hiện
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)  # Không có thanh tiêu đề
        self.setStyleSheet("background-color: rgba(0, 0, 0, 150);")  # Làm mờ nền
        self.setGeometry(200, 100, 800, 500)  # Đặt kích thước overlay

        self.btn_hide = QPushButton("Chạy Ẩn", self)
        self.btn_hide.clicked.connect(self.hide)
        self.btn_hide.setGeometry(0, 0, 900, 600)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 900, 600)

        # Tạo nút bấm
        self.btn_run = QPushButton("RUN", self)
        self.btn_run.clicked.connect(self.show_overlay)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.btn_run)
        self.setLayout(layout)

        # Khởi tạo màn hình overlay
        self.overlay = OverlayDialog(self)

    def show_overlay(self):
        """Hiển thị màn hình overlay"""
        self.overlay.show()

# Chạy ứng dụng
app = QApplication([])
window = MainWindow()
window.show()
app.exec_()
