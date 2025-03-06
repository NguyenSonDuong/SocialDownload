from dataclasses import dataclass
from datetime import datetime
@dataclass
class Video:
    video_id : str = None
    title : str = None
    kind : str = None
    publish_date : str = None
    publish_datetime : datetime = None