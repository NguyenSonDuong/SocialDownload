from dataclasses import dataclass
from datetime import datetime

class EditFrame:
    FRAME_BASE = 0
    FRAME_16_9 = 1
    FRAME_9_16 = 2
    FRAME_4_3 = 3
    
class EditCut:
    CUT_BASE = 0
    CUT_FOREARCH = 3
class EditSpeed:
    SPEED_BASE = 0
    SPEED_CUSTOM = 3
    
@dataclass    
class EditVideoSetting:
    edit_frame: int = -1
    
    speed: int = -1
    speed_custom: int = -1
    
    cut: int = -1
    cut_start: int = -1
    cut_end: int = -1
    
    folder_save: str = None
    
    intro: str = None
    outro: str = None

    video_up: str = None
    video_down: str = None

    video_left: str = None
    video_right: str = None

@dataclass    
class EditColorSetting:
    opacity: float = -1
    
    red: float = -1
    green: float = -1
    
    blue: float = -1
    brightness: float = -1
    custom_color: float = -1
    
    saturation: float = -1
    gamma: float = -1
    hue: float = -1
    
@dataclass
class EditAudioSetting:
    main_volum: int = -1
    custom_volum: int = -1
    music_path: int = -1
    custom_music_volum: int = -1
    fade_in: int = -1
    fade_out: int = -1

@dataclass
class EditSetting:
    edit_video: EditVideoSetting = None
    edit_color: EditColorSetting = None
    edit_audio: EditAudioSetting = None