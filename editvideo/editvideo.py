import subprocess
import re
import os
import unicodedata
import ffmpeg
import cv2
import numpy as np
from moviepy import concatenate_videoclips
from moviepy.video.io.VideoFileClip import VideoFileClip
import  moviepy.video.fx as vfx
from moviepy.video.VideoClip import ColorClip
from moviepy.video.compositing.CompositeVideoClip import clips_array
from editvideo.setting import EditSetting, EditAudioSetting, EditColorSetting, EditVideoSetting,EditSpeed,EditFrame,EditCut
from  proglog import ProgressBarLogger


class MyBarLogger(ProgressBarLogger):
    def __init__(self, process):
        self.process = process
        super().__init__()
    def callback(self, **changes):
        # Every time the logger message is updated, this function is called with
        # the `changes` dictionary of the form `parameter: new value`.
        for (parameter, value) in changes.items():
            print('Parameter %s is now %s' % (parameter, value))

    def bars_callback(self, bar, attr, value, old_value=None):
        # Every time the logger progress is updated, this function is called
        percentage = (value / self.bars[bar]['total']) * 100
        self.process("save_video", {
            "status": 0,
            "message": {
                "status": "downloading",
                "percent": percentage
            }
        })

class EditVideo:
    _process = None
    logger = None
    def __init__(self, setting, process):
        self.setting = EditSetting()
        self.setting = setting
        self._process = process
        self.logger = MyBarLogger(self._process)
        pass
    
    # tăng tốc độ video 
    def upSpeed(self,clip):
        try:
            if self.setting.edit_video.speed == EditSpeed.SPEED_BASE:
                return clip
            sped_up_clip = vfx.MultiplySpeed(self.setting.edit_video.speed_custom).apply(clip)
            return sped_up_clip
        except Exception as e:
            self._process("error",{
                "status": -1,
                "message": {
                    "status": "error",
                    "message": str(e)
                }
            })
            return  clip
    
    # cắt đầu hoặc cuối cảu video và cắt nỗi 5s bỏ 1s
    def cutEndStart(self, clip):
        try:
            if self.setting.edit_video.cut == EditCut.CUT_BASE:
                return clip
            if self.setting.edit_video.cut == EditCut.CUT_FOREARCH:
                return self.cut_every_5s(clip)
            if self.setting.edit_video.cut_start > 0:
                clip = clip.subclipped(self.setting.edit_video.cut_start, clip.duration)
            if self.setting.edit_video.cut_end > 0:
                clip = clip.subclipped(0, clip.duration - self.setting.edit_video.cut_end)
            return clip
        except Exception as e:
            self._process("error",{
                "status": -1,
                "message": {
                    "status": "error",
                    "message": str(e)
                }
            })
            return clip
    def cut_every_5s(self,clip):
        try:
            duration = clip.duration
            clips = []

            for start in range(0, int(duration), 5):
                end = min(start + 4, duration)
                if start < end:
                    subclip = clip.subclipped(start, end)
                    clips.append(subclip)

            final_clip = concatenate_videoclips(clips)
            return final_clip
        except Exception as e:
            self._process("error",{
                "status": -1,
                "message": {
                    "status": "error",
                    "message": str(e)
                }
            })
            return clip
    
    # chỉnh sửa khung hình videp
    
    def editFrame(self,clip):
        try:
            if self.setting.edit_video.edit_frame == EditFrame.FRAME_BASE:
                return clip


            target_width,target_height = 1920,1080
            if self.setting.edit_video.edit_frame == EditFrame.FRAME_16_9:
                target_width,target_height = 1920,1080
            if self.setting.edit_video.edit_frame == EditFrame.FRAME_9_16:
                target_width,target_height = 1080,1920
            if self.setting.edit_video.edit_frame == EditFrame.FRAME_4_3:
                target_width,target_height = 1440,1080

            def process_frame(frame):

                h, w = frame.shape[:2]
                aspect_ratio = w / h
                target_ratio = target_width / target_height
                if aspect_ratio > target_ratio:
                    # Resize theo chiều ngang
                    new_w = target_width
                    new_h = int(target_width / aspect_ratio)
                    resized_frame = cv2.resize(frame, (new_w, new_h))
                    padding_top = (target_height - new_h) // 2
                    padding_bottom = target_height - new_h - padding_top
                    padded_frame = cv2.copyMakeBorder(resized_frame, padding_top, padding_bottom, 0, 0,
                                                      cv2.BORDER_CONSTANT, value=(0, 0, 0))
                else:
                    # Resize theo chiều dọc
                    new_h = target_height
                    new_w = int(target_height * aspect_ratio)
                    resized_frame = cv2.resize(frame, (new_w, new_h))
                    padding_left = (target_width - new_w) // 2
                    padding_right = target_width - new_w - padding_left
                    padded_frame = cv2.copyMakeBorder(resized_frame, 0, 0, padding_left, padding_right,
                                                      cv2.BORDER_CONSTANT, value=(0, 0, 0))

                return padded_frame

            # Áp dụng xử lý từng frame
            new_clip = clip.image_transform(process_frame)
            return new_clip
        except Exception as e:
            self._process("error",{
                "status": -1,
                "message": {
                    "status": "error",
                    "message": str(e)
                }
            })
            return clip
    
    # thêm intro và outro
    def add_intro_outro(self, stream ):
        try:
            main_app = []
            if self.setting.edit_video.intro:
                intro_clip = VideoFileClip(self.setting.edit_video.intro)
                # intro_clip = self.editFrame(intro_clip)
                main_app.append(intro_clip)
            main_app.append(stream)
            if self.setting.edit_video.outro:
                outro_clip = VideoFileClip(self.setting.edit_video.outro)
                # outro_clip = self.editFrame(outro_clip)
                main_app.append(outro_clip)
            final_clip = concatenate_videoclips(main_app)
            return final_clip
        except Exception as e:
            self._process("error",{
                "status": -1,
                "message": {
                    "status": "error",
                    "message": str(e)
                }
            })
            return stream
    
    
   
    # Ghep trái phải trên dưới vào video
    def merge_videos(self,clip1):
        try:
        
            clip2 = None

            if self.setting.edit_video.video_left:
                clip2 = VideoFileClip(self.setting.edit_video.video_left)
            if self.setting.edit_video.video_right:
                final_clip = VideoFileClip(self.setting.edit_video.video_right)

            if self.setting.edit_video.video_up:
                final_clip = VideoFileClip(self.setting.edit_video.video_up)
            if self.setting.edit_video.video_down:
                final_clip = VideoFileClip(self.setting.edit_video.video_down)

            # Xác định thời lượng lớn nhất
            max_duration = max(clip1.duration, clip2.duration)

            # Đảm bảo cả hai video có cùng thời lượng bằng cách thêm nền đen vào video ngắn hơn
            def pad_video(clip, target_duration):
                if clip.duration < target_duration:
                    black_bg = ColorClip(size=(clip.w, clip.h), color=(0, 0, 0), duration=target_duration - clip.duration)
                    return concatenate_videoclips([clip, black_bg])
                return clip

            clip1 = pad_video(clip1, max_duration)
            clip2 = pad_video(clip2, max_duration)
            final_clip = None
            # Điều chỉnh kích thước video để có cùng chiều rộng hoặc chiều cao
            if self.setting.edit_video.video_left or self.setting.edit_video.video_right:
                new_height = min(clip1.h, clip2.h)  # Đảm bảo cùng chiều cao
                clip1 = clip1.resized(height=new_height)
                clip2 = clip2.resized(height=new_height)
                if self.setting.edit_video.video_left:
                    final_clip = clips_array([[clip2, clip1]])
                if self.setting.edit_video.video_right:
                    final_clip = clips_array([[clip1, clip2]])
            else:
                new_width = min(clip1.w, clip2.w)  # Đảm bảo cùng chiều rộng
                clip1 = clip1.resized(width=new_width)
                clip2 = clip2.resized(width=new_width)
                if self.setting.edit_video.video_up:
                    final_clip = clips_array([[clip2, clip1]])
                if self.setting.edit_video.video_down:
                    final_clip = clips_array([[clip1], [clip2]])

            return final_clip
        except Exception as e:
            self._process("error",{
                "status": -1,
                "message": {
                    "status": "error",
                    "message": str(e)
                }
            })
            return clip1

    def adjust_frame(self,frame):
        try:
            # Áp dụng opacity
            if self.setting.edit_color.opacity >0:
                frame = cv2.addWeighted(frame, self.setting.edit_color.opacity, np.zeros_like(frame), 0, 0)

            # Điều chỉnh Red, Green, Blue
            b, g, r = cv2.split(frame)
            if self.setting.edit_color.red>0:
                r = np.clip(r * self.setting.edit_color.red, 0, 255).astype(np.uint8)
            if self.setting.edit_color.green >0:
                g = np.clip(g * self.setting.edit_color.green, 0, 255).astype(np.uint8)
            if self.setting.edit_color.blue >0:
                b = np.clip(b * self.setting.edit_color.blue, 0, 255).astype(np.uint8)
            frame = cv2.merge([b, g, r])
            #chỉnh dộ sáng video
            if self.setting.edit_color.brightness >0:
                frame = np.clip(frame.astype(np.float32) + self.setting.edit_color.brightness, 0, 255).astype(np.uint8)

            # Chuyển sang không gian màu HSV để điều chỉnh saturation và hue
            if self.setting.edit_color.saturation > 0:
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV).astype(np.float32)
                hsv[:, :, 1] = np.clip(hsv[:, :, 1] * self.setting.edit_color.saturation, 0, 255)  # Saturation
                frame = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
            if self.setting.edit_color.hue >0:
                hsv[:, :, 0] = (hsv[:, :, 0] + self.setting.edit_color.hue) % 180  # Hue shift
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV).astype(np.float32)
                frame = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)

            # Áp dụng Gamma correction
            if self.setting.edit_color.gamma >0:
                inv_gamma = 1.0 / self.setting.edit_color.gamma
                table = np.array([(i / 255.0) ** inv_gamma * 255 for i in np.arange(0, 256)]).astype(np.uint8)
                frame = cv2.LUT(frame, table)
        except Exception as e:
            self._process("error",{
                "status": -1,
                "message": {
                    "status": "error",
                    "message": str(e)
                }
            })
        return frame
    def run(self, input_video):
        try:
            self._process("edit_video",{
                "status": 1,
                "message": f"Bắt đầu đọc video: {input_video}"
            })
            stream = VideoFileClip(input_video)

            self._process("edit_video",{
                "status": 1,
                "message": f"Bắt đầu thay đổi khung hình video video: {input_video}"
            })
            stream = self.editFrame(stream)
            self._process("edit_video",{
                "status": 2,
                "message": f"Đã thay đổi khung hình video: {input_video}"
            })
            self._process("edit_video",{
                "status": 1,
                "message": f"Bắt đầu tăng cắt video: {input_video}"
            })
            stream = self.cutEndStart(stream)
            self._process("edit_video",{
                "status": 2,
                "message": f"Đã ghép cắt video video: {input_video}"
            })
            self._process("edit_video",{
                "status": 1,
                "message": f"Bắt đầu tăng tốc độ video video: {input_video}"
            })
            stream = self.upSpeed(stream)
            self._process("edit_video",{
                "status": 2,
                "message": f"Đã ghép tăng tốc độ video video: {input_video}"
            })
            stream = stream.image_transform(self.adjust_frame)
            self._process("edit_video",{
                "status": 2,
                "message": f"Đã thay đổi màu sắc video: {input_video}"
            })
            self._process("edit_video",{
                "status": 1,
                "message": f"Bắt đầu thêm intro và outro nếu có vào video: {input_video}"
            })
            stream = self.add_intro_outro(stream)
            self._process("edit_video",{
                "status": 2,
                "message": f"Đã ghép introl và outro cho video: {input_video}"
            })
            self._process("edit_video",{
                "status": 1,
                "message": f"Bắt đầu ghép 2 video làm 1 video: {input_video}"
            })
            stream = self.merge_videos(stream)
            self._process("edit_video",{
                "status": 2,
                "message": f"Đã ghép 2 video làm 1 video: {input_video}"
            })
            self._process("edit_video",{
                "status": 1,
                "message": f"Bắt đầu thay đổi màu video: {input_video}"
            })
            self._process("edit_video",{
                "status": 2,
                "message": f"Đang lưu file: {input_video} ..."
            })
            stream.write_videofile(f"{self.setting.edit_video.folder_save}/{self.remove_accents()}.mp4", codec="libx264", audio_codec="aac", logger=self.logger)
        except Exception as e:
            self._process("error",{
                "status": -1,
                "message": {
                    "status": "error",
                    "message": str(e)
                }
            })


    def convert_to_mp4(self, file_path):

        # Lấy tên file mà không bao gồm đuôi file
        name_without_ext, _ = os.path.splitext(os.path.basename(file_path))
        # Tạo tên file đầu ra với đuôi .mp4
        output_file = os.path.join(self.setting.edit_video.folder_save, f"/{name_without_ext}.mp4")
        return output_file

    def remove_accents(self):
        from datetime import datetime
        now = datetime.now()
        formatted_time = now.strftime("%d_%m_%Y_%H_%M_%S")
        return f"editVideo_{formatted_time}"
