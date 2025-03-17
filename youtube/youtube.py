import requests
from datetime import datetime
import time
import random
import yt_dlp
from dotenv import load_dotenv
from config import config
from youtube.video import Video
from config.setting import TypeID, TypeChannel
from common.status import Status
from common.globalstate import GlobalStatePause, GlobalStateRun
from common.status import Status
class Youtube:
    _process = None
    def __init__(self, process, setting):
        self._process = process
        self.setting = setting
        self.isRun = GlobalStateRun()
        self.isPause = GlobalStatePause()

    def GetListVideoYoutube(self ,nextpagetoken):
        try:
            if not self.setting.id :
                raise Exception("Channel ID youtube bị trống vui lòng thêm channel id")

            base_url = config.BASE_YOUTUBE_URL
            params = {
                "part": "snippet",
                "channelId": self.setting.id,
                "order": "date",
                "maxResults": 50,
                "type": "video",
                "key": config.API_KEY
            }

            if nextpagetoken:
                params["pageToken"] = nextpagetoken

            try:    
                response = requests.get(base_url, params=params)
                data = response.json()
            except Exception as ex:
                raise Exception(f"Lỗi tải dữ liệu! kiểm tra lại kết nối Internet: {ex}")
            
            filtered_videos = []
            
            for item in data.get("items", []):
                if not self.isRun.get_value():
                    return None
                while self.isPause.get_value():
                    self._process(Status.PAUSE,{
                        "status":2,
                        "message": "Tiến trình đang tạm dừng: 2s"
                    })
                    time.sleep(2)
                video = Video(
                    video_id = item["id"]["videoId"],
                    title = item["snippet"]["title"],
                    kind = item["id"]["kind"],
                    publish_datetime = datetime.strptime(item["snippet"]["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
                )
                if self.setting.from_date and self.setting.to_date:
                    if self.setting.from_date <= video.publish_datetime <= self.setting.to_date:
                        filtered_videos.append(video)
                else:
                    filtered_videos.append(video)
            self._process(Status.START_GET_INFO,{
                "status":"0",
                "message":f"Đã lấy được {len(filtered_videos)} thành công"
            })
            nextpagetoken = data.get("nextPageToken")

            if nextpagetoken:
                return filtered_videos, nextpagetoken
            else:
                return filtered_videos, None
        except Exception as ex:
            self._process(Status.ERROR_GET_INFO,{
                "status": -1,
                "message":f"Lấy thông tin thất bại: {ex}"
            })
    def GetAllVideoChannel(self):
        infos = []
        nexttoken = ""
        self._process(Status.START_GET_INFO,{
            "status":"0",
            "message":"Bắt đầu quá trình lấy thông tin channel"
        })
        while self.status.get_value():
            if not self.isRun.get_value():
                return None
            while self.isPause.get_value():
                self._process(Status.PAUSE,{
                    "status":2,
                    "message": "Tiến trình đang tạm dừng: 2s"
                })
                time.sleep(2)
            videos, nexttoken = self.GetListVideoYoutube(nexttoken)
            if not self.isRun.get_value():
                return None
            while self.isPause.get_value():
                self._process(Status.PAUSE,{
                    "status":2,
                    "message": "Tiến trình đang tạm dừng: 2s"
                })
                time.sleep(2)
            infos.extend(videos)
            if self.setting.count > 0:
                if len(infos) >= self.setting.count:
                    break
            time.sleep(random.randint(0,2))
            if not self.status.get_value():
                break
            if not nexttoken:
                break
        return infos
    
    def get_shorts_from_channel(self):
        base_url = config.BASE_YOUTUBE_URL
        
        params = {
            "key": config.API_KEY,
            "channelId": self.setting.id,
            "part": "snippet,id",
            "maxResults": 20,
            "order": "date",
            "type": "video"
        }
        
        response = requests.get(base_url, params=params).json()
        
        shorts_videos = []
        for item in response.get("items", []):
            video_id = item["id"]["videoId"]

            # Nếu là Shorts (link có /shorts/ hoặc video < 60s)
            if self.is_short_video(video_id):
                video = Video(
                    video_id = item["id"]["videoId"],
                    title = item["snippet"]["title"],
                    kind = item["id"]["kind"],
                    publish_datetime = datetime.strptime(item["snippet"]["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
                )
                if self.setting.from_date and self.setting.to_date:
                    if self.setting.from_date <= video.publish_datetime <= self.setting.to_date:
                        shorts_videos.append(video)
                else:
                    shorts_videos.append(video)
                

        return shorts_videos

    def is_short_video(self,video_id):
        """Kiểm tra nếu video có thời lượng < 60s"""
        url = "https://www.googleapis.com/youtube/v3/videos"
    
        params = {
            "key": config.API_KEY,
            "id": video_id,
            "part": "contentDetails"
        }
        response = requests.get(url, params=params).json()
        duration = response["items"][0]["contentDetails"]["duration"]
        
        # Kiểm tra duration có nhỏ hơn 60 giây không
        return "M" not in duration  # Nếu có 'M' tức là trên 1 phút
    
    
    # def getListShort(self):
    #     if not self.isRun.get_value():
    #         return None
    #     while self.isPause.get_value():
    #         self._process(Status.PAUSE,{
    #             "status":2,
    #             "message": "Tiến trình đang tạm dừng: 2s"
    #         })
    #         time.sleep(2)
    #     options = {
    #         'quiet': True,
    #         'extract_flat': False,  # Lấy thông tin chi tiết từng video
    #     }
    #     with yt_dlp.YoutubeDL(options) as ydl:
    #         info = ydl.extract_info(f"https://www.youtube.com/channel/{self.setting.id}", download=False)  # Lấy dữ liệu từ kênh 
    #     videos = []
    #     for item in info["entries"]:
    #         video = Video(
    #                 video_id = item["id"],
    #                 title = item["title"],
    #                 kind = "")
    #         videos.append(video)
    #     return videos
    
    def download_video(self, video):
        self._process(Status.START_DOWNLOAD_ONE_VIDEO,{
                "status":2,
                "message": f"Bắt đầu tải video: {video.title}"
            })
        if not self.isRun.get_value():
                    return None
        while self.isPause.get_value():
            self._process(Status.PAUSE,{
                "status":2,
                "message": "Tiến trình đang tạm dừng: 2s"
            })
            time.sleep(2)
        ydl_opts = {
            'format': self.setting.type_download,  
            'outtmpl': '{download_folder}/%(title)s.%(ext)s'.format(download_folder=self.setting.download_folder),
            'progress_hooks': [self._download_hook],
            'quiet': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([f"https://www.youtube.com/watch?v={video.video_id}"]) 
                return True
            except Exception as ex:
                return False      
            
    def _download_hook(self,d):
        try:
            if d['status'] == 'downloading':
                if "total_bytes" not in d or "downloaded_bytes" not in d:
                    percent = float(d['downloaded_bytes']/d["total_bytes_estimate"])*100  
                else:
                    percent = float(d['downloaded_bytes']/d["total_bytes"])*100  
                self._process(Status.PROCESS_DOWNLOAD_ONE_VIDEO,{
                    "status":"0",
                    "message": {
                        "status":"downloading",
                        "percent": percent
                    }
                })
        except Exception as ex:
            self._process(Status.ERROR,{
                "status": -1,
                "message":f"Lỗi: {ex}"
            })
 

    def run(self):
        try:
            if self.setting.type_id == TypeID.CHANNEL :
                videos = []
                if self.setting.type_channel == TypeChannel.VIDEO:
                    videos = self.GetAllVideoChannel()
                    if len(videos) <=0:
                        raise Exception("Không tìm thấy video, lỗi này có thể do trong quá trình crawl data bị block, hoặc bạn không nhập đúng định dạng link vui lòng thửu lại")
                    
                elif self.setting.type_id == TypeChannel.SHORT:
                    self._process(Status.DONE_DOWNLOAD_LIST_VIDEO,{
                        "status":"0",
                        "message":"Bắt đầu lấy dữ liệu Shorts của Channel, quá trình có thể mất thời gian lâu vui lòng chờ"
                    })
                    videos = self.get_shorts_from_channel()
                    if len(videos) <=0:
                        raise Exception("Không tìm thấy video, lỗi này có thể do trong quá trình crawl data bị block, hoặc bạn không nhập đúng định dạng link vui lòng thửu lại")
                    
                success = 0
                error = 0
                if not self.isRun.get_value():
                    return None
                while self.isPause.get_value():
                    self._process(Status.PAUSE,{
                        "status":2,
                        "message": "Tiến trình đang tạm dừng: 2s"
                    })
                    time.sleep(2)
                if self.setting.count>0:
                    videos = videos[0:self.setting.count]
                for video in videos:
                    if not self.isRun.get_value():
                        return None
                    while self.isPause.get_value():
                        self._process(Status.PAUSE,{
                            "status":2,
                            "message": "Tiến trình đang tạm dừng: 2s"
                        })
                        time.sleep(2)
                    status = self.download_video(video=video)
                    if status:
                        success = success+1
                    else:
                        error = error +1
                    self._process(Status.DONE_DOWNLOAD_ONE_VIDEO,{
                        "status":"0",
                        "message":{
                            "status":"downloading",
                            "success": success,
                            "error":error,
                            "total":len(videos)
                        }
                    })
                self._process(Status.DONE_DOWNLOAD_LIST_VIDEO,{
                    "status":"0",
                    "message":"Đã tải được toàn bộ video"
                })
            elif self.setting.type_id == TypeID.LINK:
                video = Video(
                    video_id = self.setting.id,
                    title = "",
                    kind = "")
                status = self.download_video(video)
                if status:
                    self._process(Status.DONE_DOWNLOAD_ONE_VIDEO,{
                        "status":"0",
                        "message":{
                            "status":"downloading",
                            "success": 1,
                            "error":0,
                            "total":1
                        }
                    })
                    pass
                else:
                    raise Exception("")
            
        except Exception as ex:
            self._process(Status.ERROR,{
                "status": -1,
                "message":f"Lỗi: {ex}"
            })
        self._process(Status.DONE,{
            "status":2,
            "message": "HOÀN THÀNH"
        })
        


        