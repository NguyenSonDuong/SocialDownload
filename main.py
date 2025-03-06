from youtube.youtube import Youtube as yt
from config.setting import Setting, TypeDownloadYoutube, TypeID,Social
import common.helper as helper

def process(status, **kwargs):
    print("Chạy vô đây:")
    print(kwargs)

url = input("Nhập link cần tải: ")
id = helper.GetID(Social.YOUTUBE, TypeID.CHANNEL_VIDEO, url)
if not id:
    print("Lỗi không lấy được ID")
else:
    download_folder = input("Nhập đường dẫn thư mục để lưu: ")

    setting  = Setting(
        social=Social.YOUTUBE,
        type_id=TypeID.CHANNEL_VIDEO,
        download_folder=download_folder,
        id=id,
        count=10
    )
    youtube = yt(process=process,setting=setting)
    youtube.run()


