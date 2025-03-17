
class Status:
    START_GET_INFO = "start_get_info"
    PROCESS_GET_INFO = "process_get_info"
    DONE_GET_INFO = "done_get_info"
    
    START_DOWNLOAD_ONE_VIDEO = "start_download_one_video"
    PROCESS_DOWNLOAD_ONE_VIDEO = "process_download_one_video"
    DONE_DOWNLOAD_ONE_VIDEO = "done_download_one_video"
    
    START_DOWNLOAD_LIST_VIDEO = "start_download"
    DONE_DOWNLOAD_LIST_VIDEO = "done_download_list_video"
    PROCESS_DOWNLOAD_LIST_VIDEO = "process_download_video"
    
    ERROR_GET_INFO = "error_done_get_info"
    ERROR_DOWNLOAD_ONE_VIDEO = "error_done_download_one_video"
    ERROR_DOWNLOAD_LIST_VIDEO = "error_start_download"
    
    DONE = "done"
    PAUSE = "pause"
    ERROR = "error"