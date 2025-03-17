class GlobalStateRun:
    _isRun = None  # Biến giữ instance duy nhất

    def __new__(cls):
        if cls._isRun is None:
            cls._isRun = super(GlobalStateRun, cls).__new__(cls)
            cls._isRun.value = False  # Giá trị mặc định
        return cls._isRun

    def set_value(self, new_value):
        self.value = new_value

    def get_value(self):
        return self.value
    
class GlobalStatePause:
    _isPause = None  # Biến giữ instance duy nhất

    def __new__(cls):
        if cls._isPause is None:
            cls._isPause = super(GlobalStatePause, cls).__new__(cls)
            cls._isPause.value = False  # Giá trị mặc định
        return cls._isPause

    def set_value(self, new_value):
        self.value = new_value

    def get_value(self):
        return self.value