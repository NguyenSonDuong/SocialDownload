import sys
import os
from PyQt5.QtWidgets import QApplication
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'message'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'youtube'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ui'))
from ui.home import Ui_HomeWindow
from common.globalstate import GlobalStatePause,GlobalStateRun

import logging

logging.basicConfig(filename="error.log", level=logging.ERROR)

if __name__ == "__main__":
    try:
        isRun = GlobalStateRun()
        isPause = GlobalStatePause()
        app = QApplication(sys.argv)
        home = Ui_HomeWindow()
        sys.exit(app.exec_())
    except Exception as e:
        logging.error(e)
        sys.exit(1)
