from dataclasses import dataclass
from datetime import datetime

class TypeID:
    LINK = 0
    CHANNEL = 1
    
class TypeChannel:
    VIDEO = 0
    SHORT = 1

class OrderType:
    NEW = 0
    TRENDING = 1
    OLD = 2
    FOR_DATE = 3
    FOR_WEEK = 4
    FOR_TIME = 5

class Social:
    YOUTUBE = 0
    DOUYIN = 1
    WEIBO = 2
    TWITTER = 3

class TypeDownloadYoutube:
    VIDEO_HIGHTQUATITY = "bestvideo[ext=mp4]+bestaudio[ext=m4a]"
    VIDEO_BEST = "bestvideo[ext=mp4]"
    AUDIO_BEST = "bestaudio[ext=m4a]"
    VIDEO_WORST = "worstvideo[ext=mp4]"
    AUDIO_WORST = "worstaudio[ext=m4a]"
    
class TypeDownloadDoyin:
    ALL = "all"
    VIDEO = "video"
    IMAGE = "image"
    
@dataclass
class Setting:
    social: int = -1
    download_folder: str = None
    id: str = None
    type_id: int = -1
    type_channel: int = -1
    order_type: int = -1
    type_download: str = None
    from_date: datetime = None
    to_date: datetime = None
    count: int = -1
    def __dir__(self):
        return {
            "social": self.social,
            "download_folder": self.download_folder,
            "id": self.id,
            "type_id": self.type_id,
            "type_channel": self.type_channel,
            "order_type": self.order_type,
            "type_download": self.type_download,
            "from_date": self.from_date,
            "to_date": self.to_date,
            "count": self.count
        }
    def validate(self):
        if self.social not in vars(Social).values():
            return False , "Mạng xã hội chưa được hỗ trợ"
        if not self.download_folder or self.download_folder == "":
            return False , "Thư mục lưu file đang trống"
        if not self.id:
            return False , "ID đang trống vui lòng thử lại"
        if self.type_id not in vars(TypeID).values():
            return False , "loại link không hỗ trợ"
        if not self.type_download:
            return False, "Vui lòng chọn chất lượng hoặc phương thức tải"
        if self.order_type == 5 and (not self.from_date or not self.to_date):
            return False , "Vui lòng nhập đủ ngày bắt đầu và kết thúc khi chọn chọn theo ngày cụ thể"
        if self.type_channel not in vars(TypeChannel).values():
            return False , "Lựa chọn short hoặc video"
        if self.social == Social.YOUTUBE:
            if self.type_download not in vars(TypeDownloadYoutube).values():
                return False, "Loại tải không hỗ trợ"
        if self.social == Social.DOUYIN:
            if self.type_download not in vars(TypeDownloadDoyin).values():
                return False, "Loại tải không hỗ trợ"
        return True