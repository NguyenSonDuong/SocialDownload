
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import re
from config.setting import TypeID,Social

def GetID(social,typeid,url):
    id = None
    if social == Social.YOUTUBE:
        if typeid == TypeID.CHANNEL_SHORT or  typeid == TypeID.CHANNEL_VIDEO:
            link, type_link = getIdChannleYoutube(url)
            if type_link == "user":
                id = GetIdChannel(link)
            elif type_link == "id":
                id = link
            else:
                id = None
        else:
            link, type_link = getIdVideoYoutube(url)
            id = link
    return id

def getIdChannleYoutube(url):
    pattern_user = r"(https://www\.youtube\.com/@[^/]+)"
    pattern_id = r"https://www\.youtube\.com/channel/([^/]+)"

    if re.match(pattern_user, url):
        return re.match(pattern_user, url).group(1), "user"
    elif re.match(pattern_id, url):
        return re.match(pattern_id, url).group(1), "id"
    else:
        return None, "unknown"
    
def getIdVideoYoutube(url):
    # Regex cho link Shorts
    pattern_shorts = r"https://www\.youtube\.com/shorts/([\w-]+)"
    # Regex cho link Watch
    pattern_watch = r"https://www\.youtube\.com/watch\?v=([\w-]+)"

    match_shorts = re.match(pattern_shorts, url)
    match_watch = re.match(pattern_watch, url)

    if match_shorts:
        return match_shorts.group(1), "shorts"
    elif match_watch:
        return match_watch.group(1), "watch"
    else:
        return None, "unknown"
def GetIdChannel(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        meta_tag = soup.find("meta", {"property": "al:ios:url"})
        if meta_tag:
            href_value = meta_tag.get("content")
            pattern = r"www\.youtube\.com/channel/([\w-]+)"
            match = re.search(pattern, href_value)

            if match:
                channel_id = match.group(1)
                print(f"Channel ID: {channel_id}")
                return channel_id
            else:
                return None
        else:
            return None
    except Exception as ex:
        return None
    
def is_valid_youtube_handle(self,url):
    pattern = pattern = r"https?:\/\/(www\.)?youtube\.com\/@[\w\d_-]+(\/[\w\d_-]+)?$"
    return bool(re.match(pattern, url))

def extract_channel_id(self ,url):
    try:
        pattern = r"https://www\.youtube\.com/channel/([\w-]+)"
        match = re.search(pattern, url)
        return match.group(1) if match else None
    except Exception as ex:
        self._processError(str(ex), ["Youtube","extract_channel_id"])
        return None

def getTotalVideoChannel(self,url):
    try:
        if self.is_valid_youtube_handle(url):
            CHANNEL_ID = self.GetIdChannel(url)
        else:
            CHANNEL_ID = self.extract_channel_id(url)

        url = "https://www.googleapis.com/youtube/v3/channels"
        if not CHANNEL_ID:
            self._processError("Không tìm thấy channel id", ["Youtube","getTotalVideoChannel"])
            return -1
        
        params = {
            "part": "statistics",
            "id": CHANNEL_ID,
            "key": self.API_KEY
        }
        try:
            response = requests.get(url, params=params)
            data = response.json()
        except Exception as ex:
            return -1

        if "items" in data and len(data["items"]) > 0:
            video_count = data["items"][0]["statistics"]["videoCount"]
            print(f"Tổng số video trên kênh: {video_count}")
            return int(video_count)
        else:
            return -1
    except Exception as ex:
        return -1
    
from pathlib import Path

def checkDirAndCreate(path):
    path = Path(path)  # Chuyển thành đối tượng Path
    path.mkdir(parents=True, exist_ok=True)  # Tạo thư mục nếu chưa tồn tại
    print(f"Checked directory: {path}")