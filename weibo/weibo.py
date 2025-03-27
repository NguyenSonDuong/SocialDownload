import requests
from config import config
from youtube.video import Video
from config.setting import TypeID
from common.status import Status
from common.globalstate import GlobalStateRun, GlobalStatePause
import os
class Weibo:
    _process = None
    def __init__(self, process, setting):
        self._process = process
        self.setting = setting
        self.isRun = GlobalStateRun()
        self.isPause = GlobalStatePause()

    def download(self, url, path):
        headers = {
            'sec-ch-ua-platform': '"Android"',
            'X-XSRF-TOKEN': '94b475',
            'Referer': 'https://m.weibo.cn/u/5255978153',
            'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
            'sec-ch-ua-mobile': '?1',
            'MWeibo-Pwa': '1',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Mobile Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
        }
        try:
            response = requests.get(url,headers=headers)
        except Exception as e:
            raise e
        if response.status_code == 200:
            with open(path, "wb") as file:
                file.write(response.content)
            print("Ảnh đã được tải về thành công!")
        else:
            print("Không thể tải ảnh.")

    def getInfoUser(self,since_id):
        headers = {
            'sec-ch-ua-platform': '"Android"',
            'X-XSRF-TOKEN': '94b475',
            'Referer': 'https://m.weibo.cn/u/5255978153',
            'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
            'sec-ch-ua-mobile': '?1',
            'MWeibo-Pwa': '1',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Mobile Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
        }

        params = {
            'type': 'uid',
            'value': self.setting.id,
            'containerid': f'107603{self.setting.id}',
            "since_id":since_id
        }

        response = requests.get('https://m.weibo.cn/api/container/getIndex', params=params, headers=headers)
        data = response.json()
        listImage = []
        listVideo = []
        for item in data["data"]["cards"]:
            if "page_info" in item["mblog"]:
                listVideo.append(item["mblog"]["page_info"])
            if "pics" in item["mblog"]:
                for img in item["mblog"]["pics"]:
                    listImage.append(img)
        if "cardlistInfo" not in data["data"]:
            return "", listImage, listVideo
        else:
            return data["data"]["cardlistInfo"]["since_id"] if "since_id" in data["data"]["cardlistInfo"] else "", listImage, listVideo

    def GetAllPostUser(self):
        singer = ""
        images = []
        videos = []
        try:
            while self.isRun.get_value():
                singer, listImage , listVideo= self.getInfoUser(singer)
                images.extend(listImage)
                videos.extend(listVideo)
                if self.setting.count >0 and len(images)+len(videos) >= self.setting.count:
                    break
                if not singer or singer == "":
                    break       
                self._process(Status.PROCESS_GET_INFO,{
                    "status":"0",
                    "message":{
                        "status":"getInfor",
                        "step": len(images)+len(videos),
                        "total":-1
                    }
                })
            return images, videos
        except Exception as ex:
            raise ex

    def run(self):
        try:
            folder_path = f"{self.setting.download_folder}/{self.setting.id}"
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            images, videos = self.GetAllPostUser()
            count = 0
            for image in images:
                if not self.isRun.get_value():
                    return
                count = count+1
                self._process(Status.DONE_DOWNLOAD_ONE_VIDEO,{
                    "status":"0",
                    "message":{
                        "status":"downloading",
                        "success":count,
                        "error":0,
                        "total": len(images) + len(videos)
                    }
                })
                if "large" in image:
                    self.download(image["large"]["url"],f"{folder_path}/{image["pid"]}.jpg")
                else:
                    continue
            for video in videos:
                if "urls" in video:
                    count = count+1
                    self._process(Status.DONE_DOWNLOAD_ONE_VIDEO,{
                        "status":"0",
                        "message":{
                            "status":"downloading",
                            "success":count,
                            "error":0,
                            "total": len(images) + len(videos)
                        }
                    })
                    self.download(video["urls"]["mp4_hd_mp4"],f"{folder_path}/{video["object_id"].replace(":","_")}.mp4")
            self._process(Status.DONE,{
                        "status":"0",
                        "message":"Xongggg"
                    })
        except Exception as ex:
            print(ex)




