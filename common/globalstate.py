class GlobalState:
    _isRun = None  # Biến giữ instance duy nhất

    def __new__(cls):
        if cls._isRun is None:
            cls._isRun = super(GlobalState, cls).__new__(cls)
            cls._isRun.value = True  # Giá trị mặc định
        return cls._isRun

    def set_value(self, new_value):
        self.value = new_value

    def get_value(self):
        return self.value