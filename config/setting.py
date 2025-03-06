from dataclasses import dataclass
from datetime import datetime

class TypeID:
    CHANNEL_SHORT =1
    CHANNEL_VIDEO =2
    VIDEO = 3
    SHORT = 4
    

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

@dataclass
class Setting:
    social: int = Social.YOUTUBE
    download_folder: str = "Downloads"
    id: str = None
    type_id: int = TypeID.CHANNEL_VIDEO
    type_download = TypeDownloadYoutube.VIDEO_HIGHTQUATITY
    from_date: datetime = None
    to_date: datetime = None
    count: int = -1