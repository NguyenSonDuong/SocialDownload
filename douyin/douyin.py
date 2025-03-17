import asyncio
from f2.apps.douyin.handler import DouyinHandler
from f2.apps.douyin.dl import DouyinDownloader
from f2.utils.conf_manager import ConfigManager
from datetime import datetime
import os
import re
import requests
from config.setting import TypeDownloadDoyin, TypeID
import config.config as config
from common.globalstate import GlobalStatePause,GlobalStateRun
from common.status import Status
import time
class Douyin:
    _process = None
    _count = 0
    _step = 0
    def __init__(self, process, setting):
        self._process = process
        self.setting = setting
        self.isRun = GlobalStateRun()
        self.isPause = GlobalStatePause()
        

    async def getListDouyinVideoFromUser(self):
        if not self.setting.id or self.setting.id == "":
            raise Exception("ID bị trống vui lòng bổ xung lại hoặc kiểm tra định dạng link bạn nhập vào")
        videos = []
        try:
            kwargs = {
                "headers": {
                    "User-Agent": config.USER_AGENT,
                    "Referer": config.REFERER,
                },
                "proxies": {"http://": None, "https://": None},
                "mode": "post",
                "media": "video"
            } | ConfigManager(config.SOCIAL_CONFIG).get_config(config.KEY_SOCIAL)
            
            dyhandler = DouyinHandler(kwargs)
            # log thông báo tiền trình cho UI
            self._process(Status.START_GET_INFO,{
                "status": 1,
                "message":f"Bắt đầu quá trình lấy dữ liệu của user_id: {self.setting.id}"
            })
            
            # Hàm lấy thông tin user của F2
            async for aweme_list in dyhandler.fetch_user_post_videos(sec_user_id=self.setting.id):
                # Lấy status nếu true thì tiếp tục chạy nếu false thì dừng tiến trình
                if not self.isRun.get_value():
                    return None
                
                # Lấy trạng thái tạm dừng của người dùng nếu người dùng tạm dừng thì sẽ dừng trong 2s sau đó kiểm tra lại cho đến khi người dùng bắt đầu lại
                while self.isPause.get_value():
                    self._process(Status.PAUSE,{
                        "status":2,
                        "message": "Tiến trình đang tạm dừng: 2s"
                    })
                    time.sleep(2)
                
                if not aweme_list:
                    return videos
                
                temb_video = []
                
                
                if self.setting.type_download == TypeDownloadDoyin.IMAGE:
                    temb_video = [video for video in aweme_list._to_list() if video.get("aweme_type") != 0] # Nếu ngường dùng chỉ lấy video sẽ là 1 
                elif self.setting.type_download == TypeDownloadDoyin.VIDEO:
                    temb_video = [video for video in aweme_list._to_list() if video.get("aweme_type") == 0] # nếu lấy ảnh thì sẽ là 0
                else:
                    temb_video = aweme_list._to_list() # lấy toàn bộ thì không thêm điều kiện của aweme_type

                if self.setting.from_date and self.setting.to_date:
                    for video in videos:
                        create_date =  datetime.strptime(video["create_time"], "%Y-%m-%d %H-%M-%S")
                        if self.setting.from_date <= create_date <= self.setting.to_date:
                            videos.append(video)
                else:
                    videos.extend(temb_video)
                self._process(Status.PROCESS_GET_INFO,{
                    "status": 1,
                    "message":f"Lấy được {len(videos)} video của người dùng: {self.setting.id}"
                })
                if self.setting.count >0 and len(videos) >= self.setting.count:
                    videos = videos[0:self.setting.count]
                    break
                
                
            # Trả ra danh sách video
            self._process(Status.DONE_GET_INFO,{
                "status": 1,
                "message":f"Đã lấy thành công {len(videos)} video của user_id: {self.setting.id} \n BẮT ĐẦU QUÁ TRÌNH TẢI VIDEO"
            })
            
            return videos
        except Exception as ex:
            raise ex
        
    async def getInfoDouyinVideo(self):
        if not self.setting.id or self.setting.id == "":
            raise Exception("ID bị trống vui lòng bổ xung lại hoặc kiểm tra định dạng link bạn nhập vào")
        self._process(Status.START_GET_INFO,{
            "status": 1,
            "message":f"Bắt đầu quá trình lấy dữ liệu của video: {self.setting.id}"
        })
        try:
            kwargs = {
                "headers": {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
                    "Referer": "https://www.douyin.com/",
                },
                "proxies": {"http://": None, "https://": None},
            } | ConfigManager(config.SOCIAL_CONFIG).get_config(config.KEY_SOCIAL)
            if not self.isRun.get_value():
                    return None
                
                # Lấy trạng thái tạm dừng của người dùng nếu người dùng tạm dừng thì sẽ dừng trong 2s sau đó kiểm tra lại cho đến khi người dùng bắt đầu lại
            while self.isPause.get_value():
                self._process(Status.PAUSE,{
                    "status":2,
                    "message": "Tiến trình đang tạm dừng: 2s"
                })
                time.sleep(2)
            video = await DouyinHandler(kwargs).fetch_one_video(aweme_id=self.setting.id)
            self._process(Status.DONE_GET_INFO,{
                "status": 1,
                "message":f"Hoàn thành quá trình lấy thông tin video: {self.setting.id}"
            })
            return video._to_dict()
        except Exception as ex:
            self._process(Status.ERROR_DOWNLOAD_ONE_VIDEO,{
                "status": -1,
                "message":f"Lấy thông tin thất bại: {ex}"
            })

    async def downloadVideo(self, videos):
        self._process(Status.START_DOWNLOAD_LIST_VIDEO,{
                "status": 1,
                "message":f"Đang tải video"
            })
        kwargs = {
            "headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
                "Referer": "https://www.douyin.com/",
            },
            "proxies": {"http://": None, "https://": None},
            "mode": "post",
        } | ConfigManager(config.SOCIAL_CONFIG).get_config(config.KEY_SOCIAL)
        dowloader = DouyinDownloader(kwargs,self.processDownloadVideo)
        try:
            await dowloader.create_download_tasks(
                kwargs,videos, self.setting.download_folder
            )
            
        except Exception as ex:
            self._process(Status.ERROR_DOWNLOAD_ONE_VIDEO,{
                "status": -1,
                "message":f"Tải thất bại: {ex}"
            })
    def processDownloadVideo(self,type_id):
        while self.isPause.get_value():
            self._process(Status.PAUSE,{
                "status":2,
                "message": "Tiến trình đang tạm dừng: 2s"
            })
            time.sleep(2)
        self._process(Status.START_DOWNLOAD_ONE_VIDEO,{
            "status":2,
            "message": f"Bắt đầu tải video: {type_id}"
        })
        self._step = self._step+1
        self._process(Status.DONE_DOWNLOAD_ONE_VIDEO,{
            "status":"0",
            "message":{
                "status":"downloading",
                "success": self._step,
                "error":0,
                "total":self._count
            }
        })
        if self._step>= self._count:
            self._process(Status.START_DOWNLOAD_ONE_VIDEO,{
                "status": 1,
                "message":f"Tải thành công: {self._count} video"
            })
    def run(self):
        try:
            videos = []
            if self.setting.type_id == TypeID.CHANNEL:
                videos = asyncio.run(self.getListDouyinVideoFromUser())
            if self.setting.type_id == TypeID.LINK:
                video = asyncio.run(self.getInfoDouyinVideo())
                videos.append(video)
            
            if len(videos) <=0 or videos[0] == None:
                raise Exception("Không lấy được video nào vui lòng kiểm tra lại đường dẫn!")
            if not self.isRun.get_value():
                    return None
            while self.isPause.get_value():
                self._process(Status.PAUSE,{
                    "status":2,
                    "message": "Tiến trình đang tạm dừng: 2s"
                })
            self._count = len(videos)
            self._step = 0
            asyncio.run(self.downloadVideo(videos))
        except Exception as ex:
            self._process(Status.ERROR,{
                "status": -1,
                "message":f"Lỗi: {ex}"
            })
        
        self._process(Status.DONE,{
            "status":2,
            "message": "HOÀN THÀNH"
        })
    # def extract_code(url: str):
    #     match = re.search(r"https://v\.douyin\.com/([a-zA-Z0-9]+)/", url)
    #     return match.group(1) if match else None

    # def get_full_video_url(self,short_url: str):
    #     response = requests.head(f"https://v.douyin.com/{short_url}", allow_redirects=True)
    #     full_url = response.url
    #     video_id_match = re.search(r"/video/(\d+)", full_url)
    #     return video_id_match.group(1) if video_id_match else None