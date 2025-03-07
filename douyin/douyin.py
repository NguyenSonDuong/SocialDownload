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
from common.globalstate import GlobalState
class Douyin:
    _process = None
    def __init__(self, process, setting):
        self._process = process
        self.setting = setting
        self.status = GlobalState()

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
            async for aweme_list in dyhandler.fetch_user_post_videos(sec_user_id=self.setting.id):
                if not self.status.get_value():
                    break
                if not aweme_list:
                    return videos
                temb_video = []
                if self.setting.type_download == TypeDownloadDoyin.IMAGE:
                    temb_video = [video for video in aweme_list._to_list() if video.get("aweme_type") != 0]
                elif self.setting.type_download == TypeDownloadDoyin.VIDEO:
                    temb_video = [video for video in aweme_list._to_list() if video.get("aweme_type") == 0]
                else:
                    temb_video = aweme_list._to_list()

                if self.setting.from_date and self.setting.to_date:
                    for video in videos:
                        create_date =  datetime.strptime(video["create_time"], "%Y-%m-%d %H-%M-%S")
                        if self.setting.from_date <= create_date <= self.setting.to_date:
                            videos.append(video)
                else:
                    videos.extend(temb_video)

                if self.setting.count >0 and len(videos) >= self.setting.count:
                    videos = videos[0:self.setting.count]
                    break
            # Trả ra danh sách video
            return videos
        except Exception as ex:
            raise ex
        
    async def getInfoDouyinVideo(self):
        if not self.setting.id or self.setting.id == "":
            raise Exception("ID bị trống vui lòng bổ xung lại hoặc kiểm tra định dạng link bạn nhập vào")
        try:
            kwargs = {
                "headers": {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
                    "Referer": "https://www.douyin.com/",
                },
                "cookie": "YOUR_COOKIE_HERE",
                "proxies": {"http://": None, "https://": None},
            } | ConfigManager(config.SOCIAL_CONFIG).get_config(config.KEY_SOCIAL)

            video = await DouyinHandler(kwargs).fetch_one_video(aweme_id=self.setting.id)
            video._to_dict()
        except Exception as ex:
            raise ex

    async def downloadVideo(self, videos):
        kwargs = {
            "headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
                "Referer": "https://www.douyin.com/",
            },
            "proxies": {"http://": None, "https://": None},
            "mode": "post",
        } | ConfigManager(config.SOCIAL_CONFIG).get_config(config.KEY_SOCIAL)
        dowloader = DouyinDownloader(kwargs)
        try:
            await dowloader.create_download_tasks(
                kwargs,videos, self.setting.download_folder
            )
        except Exception as ex:
            raise ex

    def run(self):
        try:
            videos = []
            if self.setting.type_id == TypeID.DOUYIN_USER:
                videos = self.getListDouyinVideoFromUser()
            if self.setting.type_id == TypeID.DOUYIN_LINK:
                videos.append(self.getInfoDouyinVideo())
            
            if len(videos) <=0:
                raise Exception("Không lấy được video nào vui lòng kiểm tra lại đường dẫn!")
            if self.status.get_value():
                self.downloadVideo(videos)

        except Exception as ex:
            raise ex
        

    # def extract_code(url: str):
    #     match = re.search(r"https://v\.douyin\.com/([a-zA-Z0-9]+)/", url)
    #     return match.group(1) if match else None

    # def get_full_video_url(self,short_url: str):
    #     response = requests.head(f"https://v.douyin.com/{short_url}", allow_redirects=True)
    #     full_url = response.url
    #     video_id_match = re.search(r"/video/(\d+)", full_url)
    #     return video_id_match.group(1) if video_id_match else None