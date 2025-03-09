import time
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
from config.setting import Setting, TypeDownloadYoutube, TypeID,Social
from youtube.youtube import Youtube as yt
from douyin.douyin import Douyin as dy

app = Flask(__name__)
CORS(app)  # Cho phép React truy cập API
socketio = SocketIO(app, cors_allowed_origins="*")  # Kích hoạt WebSocket

@app.route("/run", methods=["POST"])
def download():
    data = request.get_json()
    if not data:
         return jsonify({"error": "No URL provided"}), 400
    setting = Setting(**data)


    socketio.start_background_task(download_video, setting)
    return jsonify({"message": "Kết nối thành công vui lòng chờ...."})

def download_video(setting):
    try:
        socketio.emit("progress", {"status": "Start"})
        if setting.social == Social.DOUYIN:
            douyin = dy(socketio.emit,setting)
            douyin.run()
        if setting.social == Social.YOUTUBE:
            youtube = yt(socketio.emit,setting)
            youtube.run()
        if setting.social == Social.WEIBO:
            socketio.emit("progress", {"status": "update"})
    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    socketio.run(app, port=5000, debug=True)